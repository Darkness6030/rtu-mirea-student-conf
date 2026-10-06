from django.urls import path

from sections import views

app_name = "sections"
urlpatterns = [
    path("", views.section_list, name="list"),
    path("<int:section_id>/", views.section_detail, name="detail"),
]
