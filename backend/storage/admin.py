# import os
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.urls import path, reverse
from django.utils.crypto import get_random_string
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, File
import logging

logger = logging.getLogger(__name__)

# TODO в списке пользователей также должна отображаться информация об их файловых хранилищах: количество и размер файлов, ссылка для перехода к интерфейсу управления этими файлами.

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'storage_path',
                    'file_count', 'total_file_size', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('storage_path',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('storage_path',)}),
    )

    def file_count(self, obj):
        return obj.get_file_count()

    def total_file_size(self, obj):
        return obj.get_total_file_size()

    file_count.short_description = 'Количество файлов'
    total_file_size.short_description = 'Общий размер файлов (Мб)'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/password/', self.admin_site.admin_view(self.reset_password), name='password'),
        ]
        return custom_urls + urls

    def reset_password(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        new_password = get_random_string(length=8)
        user.set_password(new_password)
        user.save()
        messages.success(request, f'Пароль для пользователя {user.username} был сброшен. Новый пароль: {new_password}')
        return redirect(reverse('admin:storage_customuser_change', args=[user_id]))

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['user', 'original_name', 'size', 'upload_date', 'last_download_date', 'comment', 'file_path', 'special_link']
    list_filter = ['user', 'original_name']

    def delete_model(self, request, obj):
        logger.debug("Удаление файла %s", obj.original_name)
        obj.delete()  # Вызываем метод delete модели
        self.message_user(request, "Файл успешно удален.")
        logger.info("Файл %s успешно удален.", obj.original_name)
