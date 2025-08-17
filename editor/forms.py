# editor/forms.py
from django.forms import ModelForm
from django import forms
from main.models import Media, Genre, Status, Type, Studio
from .models import TempMedia
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from datetime import date

class MediaForm(ModelForm):
    class Meta:
        model = TempMedia
        fields = [
            "title", "description", "type", "status",
            "start_year", "end_year", "number_of_seasons", "number_of_series",
            "genres", "studios", "cover"
        ]
        help_texts = {
            "cover": "JPG only. Will be resized to 380×562 if needed.",
        }

    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Spirited Away'}),
        label="Title in English"
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Short synopsis…'}),
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
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-select-multiple'}),
        required=False,
        label="Genres"
    )
    studios = forms.ModelMultipleChoiceField(
        queryset=Studio.objects.all(),
        required=False,
        label="Studio",
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'id_studios'})
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
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        required=False,
        label="Number of seasons"
    )
    number_of_series = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        required=False,
        label="Number of episodes"
    )
    cover = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label="Cover (JPG)"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].label_from_instance = lambda obj: obj.name
        self.fields['status'].label_from_instance = lambda obj: obj.name
        self.fields['genres'].label_from_instance = lambda obj: obj.name
        self.fields['studios'].label_from_instance = lambda obj: obj.name

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_year')
        end = cleaned.get('end_year')
        if start and end and end < start:
            self.add_error('end_year', "End date cannot be before start date.")

        # If type is Series, require positive ints when provided
        tp = cleaned.get('type')
        if tp and getattr(tp, 'name', '').lower() == 'series':
            for fld in ('number_of_seasons', 'number_of_series'):
                val = cleaned.get(fld)
                if val is not None and val <= 0:
                    self.add_error(fld, "Must be a positive number.")
        return cleaned

    def clean_cover(self):
        cover = self.cleaned_data.get('cover')
        if not cover:
            return cover
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

            return ContentFile(buffer.read(), name=cover.name)
        except Exception:
            raise forms.ValidationError("Invalid image file.")
