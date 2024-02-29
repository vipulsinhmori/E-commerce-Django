from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation
from django.db import transaction
from django.core.exceptions import ValidationError
# from django import forms
from .models import Customer  # Assuming your models are in the same app





# -----------------------------  Start CustomerRegistrationForm --------------------

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Your password can't be too similar to your other personal information and must contain at least 8 characters."
    )
    password2 = forms.CharField(
        label='Confirm password (again)',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text="Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Your password can't be too similar to your other personal information and must contain at least 8 characters."
        self.fields['password2'].help_text = "Enter the same password as before, for verification."

        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
            field.error_messages = {'required': f"{field.label} is required."}

def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
  # -----------------------------  End CustomerRegistrationForm --------------------




# ----------------------------------- Start LoginFrom -------------------------------
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        # Add your custom validation logic here
        if username and '@' in username:
            raise forms.ValidationError(_('Username should not contain "@" symbol.'), code='invalid_username')

        return cleaned_data

# ----------------------------------- End LoginFrom -------------------------------

# ----------------------------------------- Start Password  change --------------------
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus': True, 'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

# ----------------------------------------- End Password  change --------------------

# -------------------------------- PasswordResetForm --------------------------
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))
#  -------------------------EndPasswordResetForm -------------------

# -------------------------------SetPassword ----------------------------
class MySetPsswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
# ----------------------------EndSetPassword ----------------------------------

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        labels = {
            'name': _('Name'),
            'locality': _('Locality'),
            'city': _('City'),
            'state': _('State'),
            'zipcode': _('Zip Code'),
        }

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'locality': forms.TextInput(attrs={'class': 'form-control'}),
        'city': forms.TextInput(attrs={'class': 'form-control'}),
        'state': forms.Select(attrs={'class': 'form-control'}),
        'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
    }



#----------------------------send OTP-------------------------------#

# forms.py
from django import forms

class OTPVerificationForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    otp = forms.CharField(label='OTP', max_length=6, required=True)
