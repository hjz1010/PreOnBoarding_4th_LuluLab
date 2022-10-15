from django.urls import path

from reservations.views import ReservationView

urlpatterns = [
    path('', ReservationView.as_view()),
    path('/<str:reservation_number>', ReservationView.as_view())
]