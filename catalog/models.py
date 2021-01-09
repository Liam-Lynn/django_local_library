from django.db import models
import uuid
from django.shortcuts import reverse
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=128, help_text="Enter the genre of the book")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the name of book")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=500, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text="13 Character ISBN number", unique=True)
    genre = models.ManyToManyField('Genre', help_text='Enter the genre of the book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Avaliable'),
        ('r', 'Reserved')
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Avaliablity'
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_return", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    def display_id_and_book(self):
        return self.__str__()

    display_id_and_book.short_description = 'Id and book'


class Author(models.Model):
    first_name = models.CharField(max_length=100, help_text='Enter the first name of the author')
    last_name = models.CharField(max_length=100, help_text='Enter the first name of the author')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Language(models.Model):
    name = models.CharField(max_length=100, help_text='Enter the name of Language')

    def __str__(self):
        return self.name
