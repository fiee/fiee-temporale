from django.views.generic import ListView, TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'
