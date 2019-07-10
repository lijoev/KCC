from django.contrib import admin
from django.http import HttpResponse
from tablib.compat import xrange

from .models import Participants, User
from import_export import resources
# Register your models here.


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


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email')
    search_fields = ('email',)


class ParticipantsResource(resources.ModelResource):

    class Meta:
        model = Participants


admin.site.register(User, UserAdmin)
admin.site.register(Participants, ParticipantsAdmin)

