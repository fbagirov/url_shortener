from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    URLListView, URLCreateView, URLHitView,
    URLUpdateView, URLDeleteView, URLClickDistribution
)

urlpatterns = [
    path('', URLListView.as_view(), name='url-list'),
    path('new-url/', URLCreateView.as_view(), name='url-create'),
    path('url-hit/<int:url_id>', URLHitView.as_view(), name='url-hit'), # click increment view
    path('<int:url_id>', URLUpdateView.as_view(), name='url-update'), # detail and update view
    path('<int:url_id>/delete/', URLDeleteView.as_view(), name='url-delete'),

    path('<int:url_id>/hist/', URLClickDistribution.as_view(), name='url-hist')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

