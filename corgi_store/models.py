from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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
    coloring = models.CharField(max_length=5, choices=COLOR_CHOICES, default='red')
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    objects = CorgiManager()

    def __str__(self):
        return "This is {}, a {} year, {} month old {} Corgi.".format(self.name, self.age_years, self.age_months, self.coloring)

    def __repr__(self):
        return "<Corgi: {}>".format(' '.join(["{}='{}'".format(k,v) for k,v in vars(self).items() if k != '_state']))
