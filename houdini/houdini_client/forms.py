from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='email', max_length=100, widget=forms.EmailInput())
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


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
            self.add_error('confirm_email', "Emails don't match")

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['middle_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Middle Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['confirm_email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Email'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='current password', max_length=100, widget=forms.PasswordInput())
    new_password = forms.CharField(label='new password', max_length=100, widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(label='confirm new password', max_length=100, widget=forms.PasswordInput())

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "Passwords don't match")

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['new_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['confirm_new_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})


class PasswordResetForm(forms.Form):
    email = forms.CharField(label='email', max_length=100, widget=forms.EmailInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})


class PasswordSetForm(forms.Form):
    new_password = forms.CharField(label='new password', max_length=100, widget=forms.PasswordInput())
    confirm_new_password = forms.CharField(label='confirm new password', max_length=100, widget=forms.PasswordInput())

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "Passwords don't match")

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['confirm_new_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})
