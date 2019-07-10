from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'common/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)