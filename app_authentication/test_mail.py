from django.core.mail import send_mail
from django.http import HttpResponse

def send_test_email(request):
    send_mail('Test E-Mail', 'Dies ist eine Test-E-Mail.', 'videoflix@mathias-kohler.de', ['mathiaskohler@mail.de'])
    return HttpResponse('Test E-Mail wurde gesendet.')