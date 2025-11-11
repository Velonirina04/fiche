from django.contrib import admin
from .models import Fiche

@admin.register(Fiche)
class FicheAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'filiere', 'created_at')
    list_filter = ('filiere', 'created_at')
    search_fields = ('nom', 'prenom')
    ordering = ('nom', 'prenom')