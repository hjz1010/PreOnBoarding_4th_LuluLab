from django.urls import path

from reservations.views import ReservationView, ResevationListView, HospitalListView, DateTimeView

urlpatterns = [
    path('/hospitals', HospitalListView.as_view()),
	path('/list', ResevationListView.as_view()),
    path('', ReservationView.as_view()),
	path('/<str:reservation_number>', ReservationView.as_view()),
    path('/datetime/<int:hospital_id>', DateTimeView.as_view()),
	
]