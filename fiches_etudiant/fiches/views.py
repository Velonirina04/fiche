from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Fiche
from .forms import UserRegisterForm, FicheForm
from .utils import generate_pdf
import json

def is_admin(user):
    return user.is_staff or user.is_superuser

def home(request):
    return render(request, 'fiches/home.html')

class FicheListView(LoginRequiredMixin, ListView):
    model = Fiche
    template_name = 'fiches/fiche_list.html'
    context_object_name = 'fiches'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(nom__icontains=search_query) | queryset.filter(prenom__icontains=search_query)
        return queryset

class FicheDetailView(LoginRequiredMixin, DetailView):
    model = Fiche
    template_name = 'fiches/fiche_detail.html'

class FicheCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Fiche
    form_class = FicheForm
    template_name = 'fiches/fiche_form.html'
    success_url = reverse_lazy('fiche-list')
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Fiche créée avec succès!')
        return super().form_valid(form)

class FicheUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Fiche
    form_class = FicheForm
    template_name = 'fiches/fiche_form.html'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Fiche modifiée avec succès!')
        return super().form_valid(form)

class FicheDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Fiche
    template_name = 'fiches/fiche_confirm_delete.html'
    success_url = reverse_lazy('fiche-list')
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Fiche supprimée avec succès!')
        return super().delete(request, *args, **kwargs)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'fiches/register.html', {'form': form})

@login_required
def export_pdf(request, pk):
    fiche = get_object_or_404(Fiche, pk=pk)
    buffer = generate_pdf(fiche)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="fiche_{fiche.prenom}_{fiche.nom}.pdf"'
    return response

@login_required
@user_passes_test(is_admin)
def delete_multiple_fiches(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fiche_ids = data.get('fiche_ids', [])
            Fiche.objects.filter(id__in=fiche_ids).delete()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        except Exception as e:
            return HttpResponse(json.dumps({'success': False, 'error': str(e)}), content_type='application/json')
    return HttpResponse(json.dumps({'success': False}), content_type='application/json')