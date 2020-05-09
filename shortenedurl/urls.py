from django.urls import path

from .views import (
    URLListView, URLCreateView, URLHitView, URLUpdateView, URLDeleteView
)

urlpatterns = [
    path('', URLListView.as_view(), name='url-list'),
    path('new-url/', URLCreateView.as_view(), name='url-create'),
    path('url-hit/<int:url_id>', URLHitView.as_view(), name='url-hit'),
    path('<int:url_id>', URLUpdateView.as_view(), name='url-update'),
    path('<int:url_id>/delete/', URLDeleteView.as_view(), name='url-delete'),
]
