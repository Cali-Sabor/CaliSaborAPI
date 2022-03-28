from django.urls import path
from .auth import PeopleList

urlpatterns = [
    path('people/', PeopleList.as_view(), name="people_list")
]
