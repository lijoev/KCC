from django.conf.urls import include, url
from .views import LoginView, ParticipantsView, AboutUs, Mission, HomeView, DeleteParticipant, editParticipant
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    # url('', IndexView.as_view(), name='index'),
    url(r'^home/$', login_required(HomeView.as_view()), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^delete_participant/(?P<pk>\d+)/$', DeleteParticipant, name='delete_participant'),
    url(r'^edit_participant/(?P<pk>\d+)/$', editParticipant, name='edit_participant'),
    url(r'^participants/$', login_required(HomeView.as_view()), name='participants'),
    url(r'^mission/$', Mission.as_view(), name='mission'),
    url(r'^aboutus/$', AboutUs.as_view(), name='aboutus'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/user/login/'}, name='logout'),

]
