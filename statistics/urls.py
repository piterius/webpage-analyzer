from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'statistics'
urlpatterns = [
    path('', RedirectView.as_view(url='/url/')),
    path('url/', views.get_url, name='url'),
    path('statistic/', views.show_statistic, name='statistic'),
]
