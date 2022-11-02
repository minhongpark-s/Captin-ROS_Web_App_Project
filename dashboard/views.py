from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import robotData
# for timing the robotData database.
from datetime import datetime
from datetime import timedelta


from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import pytz

# for ajax request.
from django.views.decorators.csrf import csrf_exempt

def robotDataCleanUp(request):
    q = robotData.objects.all()
    q.delete()
    return redirect('databaseTest')

def databaseTest(request):
    return render(
        request,
        'dashboard/databaseTest.html',
    )

@csrf_exempt
def updateDatabase(request):
    if request.method == 'GET':
        rd = robotData()
        rd.robotPositionY = int(request.GET.get('x'))
        rd.robotPositionX = int(request.GET.get('y'))
        rd.checked_at = datetime.now()
        rd.save()
        #return redirect('databaseTest')
        return render(
            request,
            'dashboard/databaseTestSecond.html',
        )
    if request.method == 'POST':
        receive_message_x = request.POST.get('x')
        receive_message_y = request.POST.get('y')
        rd = robotData()
        rd.robotPositionY = int(receive_message_x)
        rd.robotPositionX = int(receive_message_y)
        rd.checked_at = datetime.now()
        rd.save()
        send_message = {'send_data' : "I received "+ receive_message_x + " and " + receive_message_y}
        return JsonResponse(send_message)

@csrf_exempt
def ajax_method(request):
    receive_message = request.POST.get('x')
    send_message = {'send_data' : "I received "+receive_message}
    return JsonResponse(send_message)

def showAllDatabases(request):
    rd = list(robotData.objects.all())
    return render(
        request,
        'dashboard/databaseTable.html',
        {'rd' : rd},
        )
def create1data(request):
    rd = robotData()
    rd.robotPositionY = 10
    rd.robotPositionX = 10
    rd.checked_at = datetime.now()
    rd.save()
    return render(
        request,
        'dashboard/databaseTable.html',
    )

# 현재시간의 데이터를 요청합니다.
# 현재 데이터가 없다면, 1초전의 데이터를 요청합니다.
def requestNowdata(request):
    #rd = robotData.objects.all()
    try:
        current1 = timezone.localtime(timezone.now())
        grd = robotData.objects.filter(checked_at__second=40).filter(checked_at__minute=38).filter(checked_at__hour=1)
        #grd = robotData.objects.get(checked_at=current1)
        return render(
            request,
            {'grd': grd},
            'dashboard/requestNowdata.html'
        )
    except ObjectDoesNotExist:
        logs = "first request failed."
        try:
            current2 = current1-timedelta(seconds=5)
            grd = robotData.objects.get(checked_at=current2)
            return render(
                request,
                {'grd': grd},
                'dashboard/requestNowdata.html'
            )
        except ObjectDoesNotExist:
            logs += "second request failed. "
            context = {
                'logs': logs,
                'current1' : current1,
                'current2' : current2,
            }
            return render(
                request,
                'dashboard/requestNowdata.html',
                context,
            )

def dataconnection(request):
    if request.method == 'POST':
        receive_message_x = request.POST.get('x')
        receive_message_y = request.POST.get('y')
        rd = robotData()
        rd.robotPositionY = receive_message_x
        rd.robotPositionX = receive_message_y
        rd.checked_at = datetime.now()
        rd.save()
        send_message = {'send_data' : "I received "+ receive_message_x + " and " + receive_message_y}
        return JsonResponse(send_message)

