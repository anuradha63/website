from django import forms
from django.contrib.auth.models import User
from main_app.models import StudentUserInfo, LabUserInfo, HODUserInfo, OtherUserInfo, BTPUserInfo, Department
from crispy_forms.helper import FormHelper

class StudentUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class StudentsInfoForm(forms.ModelForm):
    class Meta():
        model = StudentUserInfo
        fields = ('department','rollnumber',)


class LabUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):

        super(LabUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "<b>Username</b>"
        self.fields['email'].label = "<b>Email Address</b>"
        self.fields['password'].label = "<b>Password</b>"

class LabInfoForm(forms.ModelForm):
    class Meta():
        model = LabUserInfo
        fields = ('department',)

    def __init__(self, *args, **kwargs):

        super(LabInfoForm, self).__init__(*args, **kwargs)

        self.fields["department"].widget = forms.CheckboxSelectMultiple()
        self.fields["department"].queryset = Department.objects.all()
        self.fields['department'].label = "<b>Departments</b>"


class HODUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class HODInfoForm(forms.ModelForm):
    class Meta():
        model = HODUserInfo
        fields = ('department',)

class BTPUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class BTPInfoForm(forms.ModelForm):
    class Meta():
        model = BTPUserInfo
        fields = ('department',)

class OtherUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class OtherInfoForm(forms.ModelForm):
    class Meta():
        model = OtherUserInfo
        fields = ()
