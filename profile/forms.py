from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from profile.models import UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field



class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30,required=True,widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    avatar = forms.ImageField(widget=forms.ClearableFileInput(attrs={'placeholder': 'Avatar'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Number Phone'}))
    about_user = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'About Me'}))
    background_img = forms.ImageField(widget=forms.ClearableFileInput(attrs={'placeholder': 'Background image'}), required=False)

    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.form_method = 'POST'
    helper.form_id = "id_change_profile"
    helper.layout = Layout(
        'first_name',
        'last_name',
        'email',
        'avatar',
        HTML('<div {%if not user.get_profile.avatar%} hidden="hidden"{%endif%} id="div_preview_avatar" class="form-group"> '
             '<img id="previewImg" height="100" width="100" src="{%if user.get_profile.avatar%} {{user.get_profile.avatar.url }}{%endif%}"/> </div>'),
        'phone',
        'about_user',
        'background_img',
        Submit('save', 'Save', css_class='btn btn-lg btn-block btn-success'),
        HTML("<input type='button' value='Cancel' class='btn btn-lg btn-block btn-danger' "
             "onclick=location.href='{% url 'blog:list' user.id%}'>"),
        )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        if not self.is_bound and self.instance.pk:
            profile = self.instance.get_profile()
            self.fields['avatar'].initial = profile.avatar
            self.fields['phone'].initial = profile.phone
            self.fields['about_user'].initial = profile.about_user
            self.fields['background_img'].initial = profile.background_img

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit)
        avatar = self.cleaned_data['avatar']
        background_img = self.cleaned_data['background_img']
        phone = self.cleaned_data['phone']
        about_user = self.cleaned_data['about_user']
        user_profile=profile.get_profile()

        if avatar is False:
            user_profile.avatar.delete()
            avatar = None
        if (avatar is None) and (not user_profile.avatar):
            user_profile.avatar = None
        else:
            if avatar is None:
                pass
            else:
                user_profile.avatar = avatar

        if background_img is False:
            user_profile.background_img.delete()
            background_img = None
        if (background_img is None) and (not user_profile.background_img):
            user_profile.background_img = None
        else:
            if background_img is None:
                pass
            else:
                user_profile.background_img = background_img

        user_profile.phone = phone
        user_profile.about_user = about_user
        user_profile.save()
        return profile

