from django.urls import path

from reservations.views import ReservationView, ResevationListView, HospitalListView

urlpatterns = [
    path('/hospitals', HospitalListView.as_view()),
	path('/list', ResevationListView.as_view()),
    path('', ReservationView.as_view())
	
]