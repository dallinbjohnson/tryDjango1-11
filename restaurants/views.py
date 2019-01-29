# import code; code.interact(local=dict(globals(), **locals()))
# import ipdb; ipdb.set_trace() # pipenv install ipdb

import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.template.defaultfilters import register
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from menus.models import Item
from .forms import RestaurantLocationCreateForm
from .models import RestaurantLocation


# Create your views here.
# def Index(request):
#   template_name = 'restaurants/index.html'
#   queryset = RestaurantLocation.objects.all()
#   context = {
#     "restaurant_list": queryset,
#   }
#   return render(request, template_name, context)

class RestaurantListView(LoginRequiredMixin, ListView):
    template_name = 'restaurants/index.html'

    def get_queryset(self):
        # print(self.kwargs)
        slug = self.kwargs.get("slug")
        if slug:
            queryset = RestaurantLocation.objects.filter(
                (Q(category__iexact=slug) |
                 Q(category__icontains=slug)) and
                Q(owner=self.request.user)
            )
        else:
            queryset = RestaurantLocation.objects.filter(owner=self.request.user)
        return queryset


class RestaurantDetailView(LoginRequiredMixin, DetailView):
    template_name = 'restaurants/detail.html'

    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)

    # def get_context_data(self, *args, **kwargs):
    #   print(self.kwargs)
    #   context = super(RestaurantDetailView, self).get_context_data(*args, **kwargs)
    #   print(context)
    #   return context

    # def get_object(self, *args, **kwargs):
    #   print(self.kwargs)
    #   rest_id = self.kwargs.get('rest_id')
    #   obj = get_object_or_404(RestaurantLocation, id=rest_id) # pk=rest_id
    #   return obj


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'form.html'
    success_url = "/restaurants/"
    login_url = '/login/'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(RestaurantCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context


# @login_required(login_url='/login/')
# def restaurant_createview(request):
#   form = RestaurantLocationCreateForm(request.POST or None)
#   errors = None
#   if form.is_valid():
#     if request.user.is_authenticated():
#       instance = form.save(commit=False)
#       # customize
#       # like a pre_save
#       instance.owner = request.user
#       instance.save()
#       # like a post_save
#       return HttpResponseRedirect("/restaurants/")
#     else:
#       return HttpResponseRedirect("/login/")

#   if form.errors:
#     errors = form.errors

#   template_name = 'restaurants/form.html'
#   context = {
#       'form': form,
#       'errors': errors
#     }
#   return render(request, template_name, context)

class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'form.html'
    success_url = "/restaurants/"
    login_url = '/login/'

    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        name = self.get_object().name
        context['title'] = f'Edit Restaurant: {name}'
        return context


class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_following.all().count() == 0:
            num = None
            some_list = [
                random.randint(0, 100000),
                random.randint(0, 100000),
                random.randint(0, 100000)
            ]

            condition_bool_item = True
            if condition_bool_item:
                num = random.randint(0, 100000)

            context = {
                "num": num,
                "some_list": some_list
            }
            return render(request, 'restaurants/home.html', context)

        context = {}

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        # qs = Item.objects.filter(user__id__in=is_following_user_ids, public=True).order_by(
        #     "-updated")

        items_exists = Item.objects.filter(
            user__id__in=is_following_user_ids,
            public=True).order_by("-updated").exists()
        # qs = RestaurantLocation.objects.all()
        qs = user.is_following.all().select_related().order_by('?')

        if items_exists and qs.exists():
            context['following_users'] = qs

        return render(request, 'restaurants/home_feed.html', context)


@register.filter
def is_public(self):
    return self.filter(public=True)


@register.filter
def is_public_exists(self):
    return self.filter(public=True).exists()


@register.filter
def items_is_public(self):
    return self.filter(item__public=True).order_by('?')[:3]


class AboutView(TemplateView):
    template_name = 'restaurants/about.html'


class ContactView(TemplateView):
    template_name = 'restaurants/contact.html'
