from django.urls import path

from reservations.views import HospitalListView

urlpatterns = [
    path('/hospital', HospitalListView.as_view()),

]
