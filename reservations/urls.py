from django.urls import path

from reservations.views import HospitalListView, DateTimeView

urlpatterns = [
    path('/hospital', HospitalListView.as_view()),
    path('/datetime/<int:hospital_id>', DateTimeView.as_view()),
]
