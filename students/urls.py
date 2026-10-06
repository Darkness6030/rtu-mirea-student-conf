from django.urls import path

from students import views

app_name = "students"
urlpatterns = [
    path("", views.student_list, name="list"),
    path("<int:student_id>/", views.student_detail, name="detail"),
]
