# from django.shortcuts import render
import os
import logging
from django.utils import timezone

# from django.core.serializers import serialize
from django.http import FileResponse, Http404, HttpResponse
# from django.contrib.auth.models import User
# from django.conf import settings
# from django.template.defaulttags import comment
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import PermissionDenied
# from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import File, CustomUser
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, FileSerializer
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ['id',]
    search_fields = ['username', 'email',]
    ordering_fields = ['id', 'username',]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        logger.debug("Запрос информации о пользователе: %s", request.user.username)
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def list_users(self, request):
        logger.debug("Запрос списка пользователей администратором: %s", request.user.username)
        users = CustomUser.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        raise PermissionDenied("Доступ запрещен. Вы не можете просматривать список пользователей.")

class FileViewSet(viewsets.ModelViewSet):
    # queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    filterset_fields = ['user', 'original_name', 'upload_date', 'last_download_date', 'comment',]
    search_fields = ['user', 'original_name', 'upload_date', 'last_download_date', 'comment',]
    ordering_fields = ['id', 'user', 'original_name', 'size', 'upload_date', 'last_download_date', 'comment',]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            user_id = self.request.query_params.get('user_id', None)
            if user_id:
                return File.objects.filter(user_id=user_id)
            return File.objects.all()
        return File.objects.filter(user=user)

    def perform_create(self, serializer):
        try:
            logger.debug("Попытка загрузки файла.")
            file_obj = self.request.FILES['file_path']
            original_name = file_obj.name
            size = file_obj.size
            user = self.request.user

            file_instance = File(
                user=user,
                original_name=original_name,
                size=size,
                comment=self.request.data.get('comment', '')
            )
            file_instance.file_path = file_obj
            file_instance.save()
            logger.info("Файл '%s' успешно загружен пользователем %s.", original_name, user.username)
            return Response(FileSerializer(file_instance).data, status=status.HTTP_201_CREATED)
        except KeyError:
            logger.warning("Файл не найден в запросе.")
            return Response({"detail": "Файл не найден."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Ошибка при загрузке файла: %s", str(e))
            return Response({"detail": "Ошибка при загрузке файла."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_files(self, request):
        logger.debug("Запрос на получение файлов пользователя: %s", request.user.username)
        try:
            files = File.objects.filter(user=request.user)
            serializer = self.get_serializer(files, many=True)
            logger.info("Файлы пользователя %s успешно получены.", request.user.username)
            return Response(serializer.data)
        except ValidationError as e:
            logger.error(f"Ошибка при получении файлов: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['delete'])
    # def delete_file(self, request, pk=None):
    #     try:
    #         file = self.get_object()
    #         if file.file_path:
    #             try:
    #                 if os.path.isfile(file.file_path.path):
    #                     os.remove(file.file_path.path)
    #             except Exception as e:
    #                 return Response({"detail": f"Ошибка при удалении файла: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    #         file.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     except ValidationError as e:
    #         return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsOwnerOrReadOnly])
    def rename_file(self, request, pk=None):
        logger.debug("Запрос на переименование файла с ID %s.", pk)
        try:
            file = self.get_object()
            new_name = request.data.get('new_name', None)

            if new_name:
                file.original_name = new_name
                file.save(update_fields=['original_name'])
                logger.info("Файл с ID %s переименован в '%s'.", pk, new_name)
            return Response(FileSerializer(file).data)
        except ValidationError as e:
            logger.error("Ошибка при переименовании файла с ID %s: %s", pk, str(e))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsOwnerOrReadOnly])
    def update_comment(self, request, pk=None):
        logger.debug("Запрос на изменение комментария к файлу с ID %s.", pk)
        try:
            file = self.get_object()
            comment = request.data.get('comment', None)

            file.comment = comment
            file.save(update_fields=['comment'])
            serializer = self.get_serializer(file)
            logger.info("У файла с ID %s обновлен комментария на '%s'.", pk, comment)
            return Response(serializer.data)
            # return Response(FileSerializer(file).data)
        except ValidationError as e:
            logger.error("Ошибка при обновлении комментария к файлу с ID %s: %s", pk, str(e))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[IsOwnerOrReadOnly])
    def download_file(self, request, pk=None):
        logger.debug("Запрос на скачивание файла с ID %s.", pk)
        try:
            file = self.get_object()
            response = FileResponse(open(file.file_path.path, 'rb'), as_attachment=True, filename=file.original_name)
            file.last_download_date = timezone.now()
            file.save()
            logger.info("Файл с ID %s успешно скачан.", pk)
            return response
        except ValidationError as e:
            logger.error("Ошибка при скачивании файла с ID %s: %s", pk, str(e))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['get'])
def download_file_by_special_link(request, special_link):
    logger.debug("Запрос на скачивание файла по специальной ссылке: %s", special_link)
    try:
        file_instance = File.objects.get(special_link=special_link)
        file_path = file_instance.file_path.path

        if not os.path.exists(file_path):
            logger.warning("Файл не найден по специальной ссылке: %s", special_link)
            raise Http404("Файл не найден.")

        file_instance.last_download_date = timezone.now()
        file_instance.save()

        with open(file_path, 'rb') as f:
            logger.info("Файл с специальной ссылкой '%s' успешно скачан.", special_link)
            response = HttpResponse(f.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename="{file_instance.original_name}"'
            return response
    except File.DoesNotExist:
        logger.error("Файл с специальной ссылкой '%s' не найден.", special_link)
        raise Http404("Файл не найден.")
    except Exception as e:
        logger.error("Ошибка при скачивании файла по специальной ссылке '%s': %s", special_link, str(e))
        return Response({"detail": "Ошибка при скачивании файла."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login_user(request):
    logger.debug("Попытка входа пользователя: %s", request.data.get('username'))
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        logger.info("Успешный вход  пользователя '%s'.", username)
        return Response({'token': token.key, 'username': user.username, 'email': user.email}, status=status.HTTP_200_OK)
    logger.error("Неверные учетные данные")
    return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def register_user(request):
    logger.debug("Регистрация нового пользователя: %s", request.data.get('username'))
    username = request.data.get('username')
    email = request.data.get('email')

    if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
        logger.warning("Пользователь с именем '%s' или email '%s' уже существует.", username, email)
        return Response({"detail": "Пользователь с таким именем или email уже существует."},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        logger.info("Пользователь успешно создан")

        token, created = Token.objects.get_or_create(user=user)
        logger.info("Токен для пользователь успешно создан")
        return Response({'token': token.key, **serializer.data}, status=status.HTTP_201_CREATED)

    logger.error("Ошибка валидации данных: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
