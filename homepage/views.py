from django.http import HttpResponse


def index(request):
    return HttpResponse("Сервис организации студенческих конференций")
