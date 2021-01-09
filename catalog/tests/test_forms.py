import datetime

from django.test import TestCase
from django.utils import timezone

from catalog.forms import RenewBookForm


class RenewFormTest(TestCase):
    def test_renew_form_date_field_label(self):
        form = RenewBookForm()
        field_label = form['due_back'].label
        self.assertTrue(field_label is None or field_label == 'New Renewal Date')

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        help_text_exp = form['due_back'].help_text
        self.assertEqual(help_text_exp, "Enter a date between now and 4 weeks (Default 3)")

    def test_renew_form_date_in_past(self):
        past_date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': past_date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_more_than_4_weeks(self):
        future_date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'due_back': future_date})
        self.assertFalse(form.is_valid())

    def test_renew_form_today(self):
        today = datetime.date.today()
        form = RenewBookForm(data={'due_back': today})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'due_back': date})
        self.assertTrue(form.is_valid())