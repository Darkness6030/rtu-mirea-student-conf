from django.urls import path

from conferences import views

app_name = "conferences"
urlpatterns = [
    path("", views.conference_list, name="list"),
    path("<int:conference_id>/", views.conference_detail, name="detail"),
]
