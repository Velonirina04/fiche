from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fiches/', views.FicheListView.as_view(), name='fiche-list'),
    path('fiche/<int:pk>/', views.FicheDetailView.as_view(), name='fiche-detail'),
    path('fiche/nouveau/', views.FicheCreateView.as_view(), name='fiche-create'),
    path('fiche/<int:pk>/modifier/', views.FicheUpdateView.as_view(), name='fiche-update'),
    path('fiche/<int:pk>/supprimer/', views.FicheDeleteView.as_view(), name='fiche-delete'),
    path('fiche/<int:pk>/pdf/', views.export_pdf, name='export-pdf'),
    path('fiches/supprimer-multiple/', views.delete_multiple_fiches, name='delete-multiple-fiches'),
    path('inscription/', views.register, name='register'),
    path('connexion/', auth_views.LoginView.as_view(template_name='fiches/login.html'), name='login'),
    path('deconnexion/', auth_views.LogoutView.as_view(template_name='fiches/logout.html'), name='logout'),
]