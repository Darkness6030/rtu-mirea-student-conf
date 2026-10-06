from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("conferences/", include("conferences.urls")),
    path("students/", include("students.urls")),
    path("sections/", include("sections.urls")),
    path("talks/", include("talks.urls")),
]
handler404 = "homepage.views.page_not_found"
handler500 = "homepage.views.server_error"
