from django.urls import path

from reservations.views import HospitalListView
from reservations.views import ReservationView

urlpatterns = [
    path('/hospitals', HospitalListView.as_view()),
    path('', ReservationView.as_view())
]