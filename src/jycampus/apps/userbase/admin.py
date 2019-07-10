from django.contrib import admin
from .models import Participants, User
# Register your models here.

class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')
    search_fields = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(Participants, ParticipantsAdmin)

