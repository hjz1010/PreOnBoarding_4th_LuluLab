from xml.etree.ElementInclude import include
from django.urls import path, include

urlpatterns = [
    path('reservations', include('reservations.urls'))
]
