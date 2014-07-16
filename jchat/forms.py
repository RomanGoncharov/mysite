from django import forms
from models import Room


class CreateRoomForm(forms.Form):
    name = forms.CharField(label='Name Room', max_length=25)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Room.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Sorry, '%s' is already taken." % name)
        return name

    def save(self):
        room = Room.objects.create(name=self.cleaned_data['name'])
        return room