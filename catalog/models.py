#-*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# signal for student
from django.dispatch import receiver
from django.db.models.signals import post_save

class Student(models.Model):
    """ A model for storing student related data OneToOne with user model."""
    user = models.OneToOneField(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                    related_name="profile",
                    verbose_name="user",)
    
    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

    def get_user_email(self):
        return self.user.email
    
    def get_book_list(self):
        return '\n'.join([book.book.title for book in self.books.all()])

    get_username.short_description = 'Username'
    get_user_email.short_description = 'Email ID'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Student(user=instance)
        profile.save()


class Shelf(models.Model):
    """ Model representing a shelf in library """
    name = models.CharField(max_length=200, help_text='Enter the name of shelf')

    def __str__(self):
        return str(self.name)


class Genre(models.Model):
    """ Model for representing a book genre """
    name = models.CharField(max_length=200, help_text='Enter a book genre Ex: Fiction')

    def __str__(self):
        """ String representation of genre model """
        return self.name

class Author(models.Model):
    """ Model representing an Author """
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """ Returns url for particular author instance. """
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the model object."""
        return f'{self.first_name}, {self.last_name}'


class Book(models.Model):
    """ Model representing a book but not a specific copy of book. """
    title = models.CharField(max_length=200)
    author  = models.ManyToManyField(Author, help_text='Add a author', blank=True, related_name='copies')
    isbn = models.CharField('ISBN', 
                            max_length=13, 
                            help_text='13 Character <a href="https://www.isbn-'
                                      'international.org/content/what-isbn">ISBN number</a>',
                            null=True, blank=True)
    genre = models.ManyToManyField(Genre, help_text='Choose a genre for this book.',related_name='books')
    
    def __str__(self):
        """ String representation of model book """
        return self.title

    def get_absolute_url(self):
        """ URL for a book """
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """ Create a string to display in genre in admin site """
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    def display_author(self):
        """ Create a string to display authors in admin site """
        return ', '.join(str(author.first_name) + ' ' + str(author.last_name) for author in  self.author.all()[:3])
    
    display_genre.short_description = 'Genre'
    display_author.short_description = 'Author'

class BookInstance(models.Model):
     """ Model representing a specific copy of book that can be borrowed """
     uid = models.CharField(unique=True, 
                           max_length=250,
                           help_text='Unique id across whole library for this book.')
     book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='copies')
     due_back = models.DateField(null=True, blank=True,)
     shelf = models.ForeignKey(Shelf, on_delete=models.SET_NULL, null=True, blank=True)
     issued_to = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
          
     LOAN_STATUS = (
         ('m', 'Maintenance'),
         ('o', 'On Loan'),
         ('a', 'Available'),
         ('r', 'Reserved'),
         ('d', 'Due'),
     )
     status = models.CharField(
         max_length = 1,
         choices = LOAN_STATUS,
         blank=True,
         default='a',
         help_text='Book Availability',
     )
     class Meta:
         ordering =['due_back']
         verbose_name_plural = 'Book Copies'
         verbose_name = 'Copy'
    
     def __str__(self):
        """ String representation for model object. """
        return f'{self.book.title} {str(self.id)[:15]}'

     def update_status(self):
         """ Checks if a book is due for more than 15 days and marks it due. """
         if (timezone.datetime.today() - timezone.datetime(self.due_back.year, self.due_back.month, self.due_back.day)).days >= 15:
             print('This copy is due for return.')
             self.status = 'd'
             self.save()
    