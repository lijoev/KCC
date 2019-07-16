from django.contrib import admin
from django.http import HttpResponse
from tablib.compat import xrange
from .models import Participants, User
from import_export import resources
# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField



from django.contrib.auth.admin import UserAdmin
def export_xls(modeladmin, request, queryset):
    import xlwt
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=participants.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Participants")

    row_num = 0

    columns = [
        (u"ID", 2000),
        (u"Name", 6000),
        (u"Email", 8000),
        (u"Phone Number", 8000),
        (u"College", 8000),
        (u"Stream", 8000),
        (u"Subregion", 8000),
        (u"Zone", 8000),
        # (u"Dob", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in queryset:
        row_num += 1
        row = [
            obj.pk,
            obj.name,
            obj.email,
            obj.phoneNumber,
            obj.college,
            obj.stream,
            obj.subregion,
            obj.zone,
            # obj.dob,
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


export_xls.short_description = u"Export XLS"


class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','phoneNumber', 'college', 'stream', 'subregion', 'zone', 'dob')
    list_filter = ('name', 'email', 'college', 'stream', 'subregion', 'zone')
    search_fields = ('name',)
    actions = [export_xls]


# class UserAdminManager(admin.ModelAdmin):
#     list_display = ('full_name', 'email')
#     search_fields = ('email',)


class ParticipantsResource(resources.ModelResource):

    class Meta:
        model = Participants


# admin.site.register(User, UserAdminManager)
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('email', 'password', 'is_staff', 'is_active', 'first_name')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'is_active')
    # list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'full_name', 'nick_name')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions',)}),
        ('Important Dates', {'fields': ('date_joined',)}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    list_filter = ('date_joined', 'is_active', 'is_superuser', 'is_staff',)



admin.site.register(User, UserAdmin)
admin.site.register(Participants, ParticipantsAdmin)
