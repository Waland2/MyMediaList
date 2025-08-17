from django.forms import ModelForm
from django import forms

from main.models import Media, Genre, Status, Type, Studio
from .models import TempMedia
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image


class MediaForm(ModelForm):
    class Meta:
        model = TempMedia
        fields = [
            "title", "description", "type", "status",
            "start_year", "end_year", "number_of_seasons", "number_of_series",
            "genres", "studios", "cover"
        ]

    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Title in English"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False,
        label="Description"
    )

    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Type"
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status"
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="Genres"
    )
    studios = forms.ModelMultipleChoiceField(
        queryset=Studio.objects.all(),
        required=False,
        label="Studio"
    )

    start_year = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label="Start date"
    )
    end_year = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False,
        label="End date"
    )
    number_of_seasons = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,
        label="Number of seasons"
    )
    number_of_series = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False,
        label="Number of episodes"
    )
    cover = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label="Cover (JPG format)"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].label_from_instance = lambda obj: obj.name
        self.fields['status'].label_from_instance = lambda obj: obj.name
        self.fields['genres'].label_from_instance = lambda obj: obj.name

    def clean_cover(self):
        cover = self.cleaned_data.get('cover')
        if cover:
            if not cover.name.lower().endswith('.jpg'):
                raise forms.ValidationError("Only JPG files are allowed.")

            try:
                img = Image.open(cover)
                img = img.convert('RGB')

                if img.size != (380, 562):
                    img = img.resize((380, 562), Image.LANCZOS)

                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                buffer.seek(0)

                cover = ContentFile(buffer.read(), name=cover.name)
            except Exception:
                raise forms.ValidationError("Invalid image file.")
        return cover
