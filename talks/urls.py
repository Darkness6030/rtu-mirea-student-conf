from django.urls import path

from talks import views

app_name = "talks"
urlpatterns = [
    path("", views.talk_list, name="list"),
    path("<int:talk_id>/", views.talk_detail, name="detail"),
]
