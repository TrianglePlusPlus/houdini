from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='email', max_length=100, widget=forms.EmailInput())
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput())


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='first name', max_length=32)
    middle_name = forms.CharField(label='middle name', max_length=32, required=False)
    last_name = forms.CharField(label='last name', max_length=32)
    email = forms.CharField(label='email', max_length=100, widget=forms.EmailInput())
    confirm_email = forms.CharField(label='confirm email', max_length=100, widget=forms.EmailInput())
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='confirm password', max_length=100, widget=forms.PasswordInput())

    # TODO: CAPSHCKA?

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


class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='current password', max_length=100, widget=forms.PasswordInput())
    new_password = forms.CharField(label='new password', max_length=100, widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(label='confirm new password', max_length=100, widget=forms.PasswordInput())

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password and new_password != confirm_new_password:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data


class PasswordResetForm(forms.Form):
    email = forms.CharField(label='email', max_length=100, widget=forms.EmailInput())


class PasswordSetForm(forms.Form):
    new_password = forms.CharField(label='new password', max_length=100, widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(label='confirm new password', max_length=100, widget=forms.PasswordInput())

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password and new_password != confirm_new_password:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data
