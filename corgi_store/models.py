from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = user.email
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )

class CorgiManager(models.Manager):
    def create_corgi(self, name, **kwargs):
        return self.create(name, **kwargs)

class Corgi(models.Model):
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('rh-tc', 'Red-Headed Tricolor'),
        ('bh-tc', 'Black-Headed Tricolor'),
        ('sable', 'Sable'),
        ('fawn', 'Fawn'),
        ('other', 'Other')
    ]
    name = models.CharField(max_length=120)
    age_years = models.IntegerField(default=0)
    age_months = models.IntegerField(default=0)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('X', 'Other')], default='X')
    coloring = models.CharField(max_length=120, choices=COLOR_CHOICES, default='red')
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    objects = CorgiManager()

    def __str__(self):
        return "This is {}, a {} year, {} month old {} Corgi.".format(self.name, self.age_years, self.age_months, self.coloring)

    def __repr__(self):
        return "<Corgi: {}>".format(' '.join(["{}='{}'".format(k,v) for k,v in vars(self).items() if k != '_state']))

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    corgi = models.ForeignKey(Corgi, on_delete=models.CASCADE)
    price = models.IntegerField()
    contact = models.CharField(max_length=300)
    open = models.BooleanField(default=True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    corgi = models.ForeignKey(Corgi, on_delete=models.CASCADE)
