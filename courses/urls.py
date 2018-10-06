# from django.conf.urls import url   <--- Outdated??
from django.urls import path

from . import views

urlpatterns = [
    path("", views.course_list),
    path("<int:pk>/", views.course_detail),
    #path('<int:pk>/', name='course_detail'),  # Käbbel?
]