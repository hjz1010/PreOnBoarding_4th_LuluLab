from django.urls import path

from reservations.views import ResevationListView

urlpatterns = [
	path('/list', ResevationListView.as_view()),
]