import datetime
import os

import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from shortenedurl.forms import URLCreateForm
from shortenedurl.models import URL, Access, ClickedDistribution
from url_shortener.settings import BASE_DIR


class URLListView(LoginRequiredMixin, generic.ListView):
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    model = URL
    queryset = URL.objects.select_related('created_by').all()
    template_name = 'url_list.html'
    extra_context = {'title': 'SHORTENED URLS'}


class URLCreateView(LoginRequiredMixin, generic.CreateView):
    model = URL
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    form_class = URLCreateForm
    success_url = reverse_lazy('url-list')
    template_name = 'url_create.html'
    extra_context = {'title': 'CREATE A NEW SHORTENED URL'}


class URLHitView(LoginRequiredMixin, generic.View):
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request, url_id, *args, **kwargs):
        url_instance = get_object_or_404(URL, pk=url_id)
        url_instance.clicked()

        access_instance, created = Access.objects.get_or_create(
            user_id=request.user.id, url=url_instance
        )
        access_instance.clicked()

        ClickedDistribution.objects.create(
            user_id=request.user.id, url=url_instance
        )

        return redirect(url_instance.full_url)


class URLUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    model = URL
    form_class = URLCreateForm
    template_name = 'url_detail.html'
    pk_url_kwarg = 'url_id'
    context_object_name = 'url'
    success_url = reverse_lazy('url-list')


class URLDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    model = URL
    pk_url_kwarg = 'url_id'
    template_name = 'url_confirm_delete.html'
    success_url = reverse_lazy('url-list')


class URLClickDistribution(LoginRequiredMixin, generic.View):
    login_url = '/admin/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'url_histogram.html'

    def get(self, request, url_id, *args, **kwargs):
        url_instance = get_object_or_404(URL, id=url_id)
        now = datetime.datetime.now()
        delta = now.today() - datetime.timedelta(days=30)

        instances = list(
            ClickedDistribution.objects.filter(
                url=url_instance,
                clicked_at__range=(
                    delta, now.today() + datetime.timedelta(days=1)
                )
            ).values('clicked_at')
        )
        return render(
            request, self.template_name,
            context={
                'image': self._create_histogram(instances, now),
                'url_object': url_instance
            }
        )

    @staticmethod
    def _organize_data(instances):
        today = datetime.datetime.today()
        organized_data = {
            (today - datetime.timedelta(days=x)).date(): 0 for x in range(30)
        }

        for instance in instances:
            clicked_at_date = instance.get('clicked_at').date()
            if clicked_at_date in organized_data:
                organized_data[clicked_at_date] += 1

        return list(organized_data.values())

    def _create_histogram(self, instances, now):
        series = pd.Series(self._organize_data(instances))
        print(series)
        filename = f'hist-{now.strftime("%Y-%m-%d-%H-%M-%S")}.png'
        histogram = series.hist()
        figure = histogram.get_figure()
        figure.savefig(os.path.join(
            BASE_DIR, 'url_shortener', 'static', filename)
        )

        return filename
