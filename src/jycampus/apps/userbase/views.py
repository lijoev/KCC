from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
try:
    from django.utils import simplejson as json
except ImportError:
    import json
import logging
from braces.views import AnonymousRequiredMixin
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import LoginForm, AddParticipantsForm
from .models import Participants
from django.contrib import messages

User = get_user_model()

LOG = logging.getLogger('myStock.%s' % __name__)

# Create your views here.


class LoginView(AnonymousRequiredMixin, TemplateView):
    """
    Login view class. Users are logged in
    using either email or nick name.
    """

    login_form = LoginForm
    initial = {'key': 'value'}
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        """
        function which return the template with login and signup form
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        login_form = self.login_form(initial=self.initial)

        context = {
            'login_form': login_form,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        function which handles post request from login and signup form
        to login and create user
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        login_form = self.login_form(request.POST)
        context = {
            'login_form': login_form,

        }
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            raw_password = login_form.cleaned_data.get('password')
            try:
                user = authenticate(email=email, password=raw_password)
                print(user)
                login(request, user)
                return redirect('/user/home')
            except:
                messages.warning(request, 'Email And Password Does Not Match.')
                return redirect('/user/login')
        return render(request, self.template_name, context)


class ParticipantsView(TemplateView):
    participants_form = AddParticipantsForm
    # sign_up_form = SignUpForm
    initial = {'key': 'value'}
    template_name = 'registration/adduser.html'

    def get(self, request, *args, **kwargs):
        """
        function which return the template with login and signup form
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        participants_form = self.participants_form(initial=self.initial)

        context = {
            'participants_form': participants_form,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        """

        :param request:
        :return:
        """
        participants_form = self.participants_form(request.POST)

        if participants_form.is_valid():
            sub_region = participants_form.cleaned_data.get('subregion')
            try:
                participants_form.save()
                return redirect('/user/home')
            except ValidationError as e:
                print(e)
                pass
        context = {
            'participants_form': participants_form,

        }
        return render(request, self.template_name, context)


class ParticipantList(TemplateView):
    """

    """
    template_name = 'registration/dashboard.html'

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        participants_list = Participants.objects.all()
        paginator = Paginator(participants_list, 4)
        page = request.GET.get('page', 1)

        try:
            participants = paginator.page(page)
        except PageNotAnInteger:
            participants = paginator.page(1)
        except EmptyPage:
            participants = paginator.page(paginator.num_pages)
        context = {
            'participants': participants
        }
        print(participants)
        return render(request, self.template_name, context)


def DeleteParticipant(request, pk):
    """

    """
    print(pk)
    participant_object = Participants.objects.get(id=pk)

    if participant_object:

        participant_object.delete()
    return redirect("/user/home")


def editParticipant(request, pk):
    instance = get_object_or_404(Participants, id=pk)
    participant_form = AddParticipantsForm(request.POST or None, instance=instance)
    if participant_form.is_valid():
        participant_form.save()
        return redirect("/user/home")
    return render(request, 'registration/adduser.html', {'participants_form': participant_form})


class AboutUs(TemplateView):
    """

    """
    template_name = 'registration/about.html'

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return render(request, self.template_name)


class Mission(TemplateView):
    """

    """
    template_name = 'registration/mission.html'

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return render(request, self.template_name)


class HomeView(TemplateView):
    """

    """
    template_name = 'registration/participants.html'

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        participants_list = Participants.objects.all()
        paginator = Paginator(participants_list, 10)
        page = request.GET.get('page', 1)

        try:
            participants = paginator.page(page)
        except PageNotAnInteger:
            participants = paginator.page(1)
        except EmptyPage:
            participants = paginator.page(paginator.num_pages)
        context = {
            'participants': participants
        }
        print(participants)
        return render(request, self.template_name, context)


