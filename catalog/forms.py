import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from catalog.models import BookInstance


class RenewBookForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _("New Renewal Date")}
        help_texts = {'due_back': _("Enter a date between now and 4 weeks (Default 3)")}

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_("The renewal date must not be in the past"))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("The renewal date must not be more than 4 weeks"))

        return data
