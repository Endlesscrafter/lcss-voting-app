from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('election/<str:wahl>', views.election),
    path('abgeschlossen', views.abgeschlossen)
]
