from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Item
from .forms import ItemForm


# Create your views here.
class ItemListView(LoginRequiredMixin, ListView):
  template_name = 'menus/index.html'

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user)


class ItemDetailView(LoginRequiredMixin, DetailView):
  template_name = 'menus/detail.html'

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user)


class ItemCreateView(LoginRequiredMixin, CreateView):
  template_name = 'form.html'
  form_class = ItemForm

  def form_valid(self, form):
    obj = form.save(commit=False)
    obj.user = self.request.user
    return super(ItemCreateView, self).form_valid(form)

  def get_form_kwargs(self):
    kwargs = super(ItemCreateView, self).get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user)

  def get_context_data(self, *args, **kwargs):
    context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
    context['title'] = 'Create Menu Item'
    return context


class ItemUpdateView(LoginRequiredMixin, UpdateView):
  template_name = 'form.html'
  form_class = ItemForm

  def get_form_kwargs(self):
    kwargs = super(ItemUpdateView, self).get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

  def get_queryset(self):
    return Item.objects.filter(user=self.request.user)

  def get_context_data(self, *args, **kwargs):
    context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
    context['title'] = 'Edit Menu Item'
    return context