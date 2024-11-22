# from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'storage_path')

# class CustomUserForm(forms.ModelForm):
#     # username = forms.CharField(label='Имя пользователя', max_length=150)
#     # password = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
#     # first_name = forms.CharField(label='Имя', max_length=30, required=False)
#     # last_name = forms.CharField(label='Фамилия', max_length=30, required=False)
#     # email = forms.EmailField(label='Адрес электронной почты', required=False)
#
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'first_name', 'last_name', 'email', 'password', 'storage_path', 'is_active', 'is_staff', 'is_superuser']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }

# class UserProfileForm(forms.ModelForm):
#     username = forms.CharField(label='Имя пользователя', max_length=150)
#     password = forms.CharField(label='Пароль', widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False)
#     first_name = forms.CharField(label='Имя', max_length=30, required=False)
#     last_name = forms.CharField(label='Фамилия', max_length=30, required=False)
#     email = forms.EmailField(label='Адрес электронной почты', required=False)
#
#     class Meta:
#         model = UserProfile
#         fields = ['username', 'first_name', 'last_name', 'email', 'password', 'storage_path', 'is_active', 'is_staff', 'is_admin']
#
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         if self.instance and self.instance.user:
#             self.fields['username'].initial = self.instance.user.username
#             self.fields['password'].initial = self.instance.user.password
#             self.fields['first_name'].initial = self.instance.user.first_name
#             self.fields['last_name'].initial = self.instance.user.last_name
#             self.fields['email'].initial = self.instance.user.email
#
#     def save(self, commit=True):
#         user_profile = super(UserProfileForm, self).save(commit=False)
#         user = user_profile.user
#         user.username = self.cleaned_data['username']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
#         if self.cleaned_data['password']:
#             user.set_password(self.cleaned_data['password'])
#         if commit:
#             user.save()
#             user_profile.save()
#         return user_profile
