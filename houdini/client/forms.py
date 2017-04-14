from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='email', max_length=100, widget=forms.EmailInput())
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput())

class RegisterForm(forms.Form):
    email = forms.CharField(label='email', max_length=100, widget=forms.EmailInput())
    confirm_email = forms.CharField(label='confirm email', max_length=100, widget=forms.EmailInput())
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='confirm password', max_length=100, widget=forms.PasswordInput())

    # CAPSHCKA?

    def clean(self):
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')
        if email and email != confirm_email:
            raise forms.ValidationError("Emails don't match")

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data
