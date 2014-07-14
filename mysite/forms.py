from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.forms import AuthenticationForm


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field

class CustomRegForm (RegistrationFormUniqueEmail):

    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.form_method = 'POST'
    helper.form_id = "id_registration"
    helper.layout = Layout(
        'username',
        'email',
        'password1',
        'password2',
         Submit('signin', 'Sign up', css_class='btn btn-lg btn-block btn-success'),
            HTML("<input type='button' value='Cancel' class='btn btn-lg btn-block btn-danger' "
                 "onclick=location.href='{% url 'authorisation:auth_login' %}'>"),
            )


class CustomAuthForm(AuthenticationForm):

    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.form_method = 'POST'
    helper.form_id = "id_auth"
    helper.layout = Layout(
        'username',
        'password',
         Submit('signin', 'Sign in', css_class='btn btn-lg btn-block btn-success')
            )
