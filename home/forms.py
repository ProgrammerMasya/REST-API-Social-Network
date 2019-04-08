from django import forms
from django.contrib.auth.models import User

from home.models import Post


class PostsForm(forms.ModelForm):
    post = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Write a new post:"}
        )
    )

    class Meta:
        model = Post
        fields = ("post",)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password_check",
            "first_name",
            "last_name",
            "email",
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Логин"
        self.fields["password"].label = "Пароль"
        self.fields["password"].help_text = "Придумайте Пароль"
        self.fields["password_check"].label = "Повторите Пароль"
        self.fields["first_name"].label = "Имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["email"].label = "Ваша почта"
        self.fields["email"].help_text = "Пожалуйста, указывайте реальный адрес"

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        password_check = self.cleaned_data["password_check"]
        email = self.cleaned_data["email"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Пользователь с данным логином уже " "зарегистрирован в системе!"
            )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с данным почтовым " "адресом уже зарегистрирован!"
            )
        if password != password_check:
            raise forms.ValidationError("Ваши пароли не совпадают! " "Попробуйте снова")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Логин"
        self.fields["password"].label = "Пароль"

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Пользователь с данным логином не " "зарегистрирован в системе!"
            )

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError("Неверный пароль!")
