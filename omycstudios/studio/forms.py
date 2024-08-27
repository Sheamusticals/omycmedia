
from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phoneNumber', 'message']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commenter_name', 'commenter_email', 'comment']

class BookingForm(forms.ModelForm):
    CHOICE_OPTIONS = [
        ('live_stream', 'Live Stream'),
        ('video_editing', 'Video Editing'),
         ('Event Planning', 'Event Planning')
    ]

    service_type = forms.ChoiceField(choices=CHOICE_OPTIONS, widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = Booking
        fields = ['name', 'address', 'event', 'date', 'time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'event': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'service_type': forms.Select(choices=Booking.SERVICE_TYPE_CHOICES, attrs={'class': 'form-control'}),
        }
class RadioForm(forms.ModelForm):
    class Meta:
        model = Radio_Comment
        fields = ['content']