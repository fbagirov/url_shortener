from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from shortenedurl.forms import URLCreateForm
from shortenedurl.models import URL


class URLListView(generic.ListView):
    model = URL
    template_name = 'url_list.html'
    extra_context = {'title': 'SHORTENED URLS'}


class URLCreateView(generic.CreateView):
    model = URL
    form_class = URLCreateForm
    success_url = reverse_lazy('url-list')
    template_name = 'url_create.html'
    extra_context = {'title': 'CREATE A NEW SHORTENED URL'}


class URLHitView(generic.View):

    def get(self, request, url_id, *args, **kwargs):
        url_instance = URL.objects.get(pk=url_id)
        url_instance.clicked()
        return redirect(url_instance.full_url)


class URLUpdateView(generic.UpdateView):
    model = URL
    form_class = URLCreateForm
    template_name = 'url_detail.html'
    pk_url_kwarg = 'url_id'
    context_object_name = 'url'
    success_url = reverse_lazy('url-list')


class URLDeleteView(generic.DeleteView):
    model = URL
    pk_url_kwarg = 'url_id'
    template_name = 'url_confirm_delete.html'
    success_url = reverse_lazy('url-list')
