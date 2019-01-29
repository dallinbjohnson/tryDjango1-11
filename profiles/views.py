from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, View, CreateView, ListView

from menus.models import Item
from profiles.forms import Registerform
from profiles.models import Profile
from restaurants.models import RestaurantLocation

User = get_user_model()


# Create your views here.
def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
                return redirect("/login/")
    return redirect("/login/")


class RegisterView(CreateView):
    form_class = Registerform
    template_name = 'registration/register.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     return redirect("/logout/")
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


class ProfileListView(ListView):
    template_name = 'profiles/user_list.html'
    model = Profile

    def get_queryset(self):
        qs = Profile.objects.all().exclude(user__id=self.request.user.id).order_by('user__username')
        if self.request.GET.get('q'):
            qs = Profile.objects.filter(
                Q(user__username__iexact=self.request.GET.get('q')) |
                Q(user__username__icontains=self.request.GET.get('q'))
            ).exclude(user__id=self.request.user.id).order_by('user__username')
        return qs


class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username").strip()
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)

        return redirect(f"/profile/{profile_.user.username}")


class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']

        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following

        query = self.request.GET.get('q')
        items_exists = Item.objects.filter(user=user).exists()
        qs = RestaurantLocation.objects.filter(owner=user)
        qs = qs.search(query)

        if items_exists and qs.exists():
            context['locations'] = qs

        return context
