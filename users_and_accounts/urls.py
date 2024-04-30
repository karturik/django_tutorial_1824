from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.register_request, name="register"),
    path('edit/', views.edit, name='edit'),
    re_path(r'^profile/(?P<pk>\d+)$', views.ProfileDetailView.as_view(), name='profile_page'),
]