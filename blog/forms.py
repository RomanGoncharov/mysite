from django import forms
from blog.models import BlogPost, PostComment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, FieldWithButtons, InlineField, StrictButton


class AddNote(forms.ModelForm):

    helper = FormHelper()
    helper.form_class = 'form-group'
    helper.form_method = 'POST'
    helper.form_id = "id_change_post"
    helper.error_text_inline = True
    helper.layout = Layout(
            'title',
            'body',
            Submit('save', 'Save', css_class='btn btn-lg btn-block btn-success'),
            HTML("<input type='button' value='Cancel' class='btn btn-lg btn-block btn-danger' "
                 "onclick=location.href='{% url 'blog:list' user.id%}'>"),
            )
    def clean_body(self):
        data = self.cleaned_data['body']
        if len(data) > 255:
            raise forms.ValidationError("The maximum message length should be no more 255 simbols!")
        return data
    class Meta:
        model = BlogPost
        fields = ('title', 'body')


class PostCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Comment...'}))

    class Meta:
        model = PostComment
        fields = ['comment']

    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = "form-group"
    helper.form_show_labels = False
    helper.error_text_inline = True
    helper.field_template = 'bootstrap3/layout/inline_field.html'
    helper.layout = Layout(Field('comment', rows="4", css_class='form-control'),
                           Submit('send', 'Send!', css_class="btn  btn-success"))



