from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Fiche(models.Model):
    FILIERE_CHOICES = [
        ('Informatique', 'Informatique'),
        ('Economie', 'Economie'),
        ('Droit', 'Droit'),
        ('Langue Etrangere applique', 'Langue Etrangere Applique'),
        ('Education', 'Education'),
        ('Communication', 'Communication'),
        ('Agronomie', 'Agronomie'),
    ]
    niveau_CHOICES=[('L2','L2'),('L3','L3')]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    filiere = models.CharField(max_length=100, choices=FILIERE_CHOICES)
    niveau = models.CharField(max_length=10, choices=niveau_CHOICES)
    interets = models.TextField(blank=True)
    description = models.TextField(blank=True)
    avis_responsable = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def get_absolute_url(self):
        return reverse('fiche-detail', kwargs={'pk': self.pk})