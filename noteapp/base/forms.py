from django.forms import ModelForm
from .models import Note

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        #fields = ["title", "text", "private"]
