from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='candidate_index'),
]
