from django import forms
from .models import Post, Suggestion
from taggit.models import Tag
from django.core.exceptions import ValidationError
#from dal import autocomplete

class TestForm(forms.ModelForm):
    def clean_file(self, form):
        megabyte_limit = 5.0
        media = self.cleaned_data.get('media', False)
        print(media._size)
        if media._size > megabyte_limit * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    #tags = forms.ModelChoiceField(queryset=Tag.objects.all(), widget=autocomplete.TaggitSelect2('tag-autocomplete'))
    class Meta:
        model = Post
        #fields = ('__all__')
        fields = ['title', 'content', 'media', 'tags']




class SuggestionForm(forms.ModelForm):

    class Meta:
        model = Suggestion
        fields = ['title', 'content']