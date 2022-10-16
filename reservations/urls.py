from django.urls import path

from reservations.views import ReservationView
from reservations.views import HospitalListView

urlpatterns = [
    path('/hospitals', HospitalListView.as_view()),
    path('', ReservationView.as_view()),
    path('/<str:reservation_number>', ReservationView.as_view())
]