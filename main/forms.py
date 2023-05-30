from django import forms
from .models import Post

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,SetPasswordForm
from django.contrib.auth.models import User
 
class RegisterForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=("username","email","password1","password2")
        help_text={
            "password1":None,
            "password2":None,
        }

        username=forms.CharField(widget=forms.TextInput())
        email=forms.EmailField(widget=forms.TextInput(attrs={
            'class':'text-dark p-2 form-control ',
            'placeholder':'enter your email'
        }))

     #hi nmeadd ndi ieke stuff na placeholder  
    def __init__(self, *args, **kwargs):#field zmekua generated by the default USER form ya django
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control m-1', 'placeholder': 'enter password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control m-1', 'placeholder': 'confirm pasword'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control m-1', 'placeholder': 'enter email'})
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control m-1', 'placeholder': ' enter username'})
        

    def save(self,commit=True):
        user=super(RegisterForm, self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user

class AuthForm(AuthenticationForm):
    class Meta:
        model=User
        fields=("username","password")
    def __init__(self, *args, **kwargs):#field zmekua generated by the default USER form ya django
            super(AuthForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control m-1', 'placeholder': 'username'})
            self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control m-1', 'placeholder': 'password'})

#create a new form
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=("title","note")

#recover password
class NewPassForm(SetPasswordForm):
    model=User
    fields=('new password','confirm password')

class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title","note")
    def save(self,commit=True):
        note=super(PostForm, self).save()
        if commit:
            form.save()
        return note
