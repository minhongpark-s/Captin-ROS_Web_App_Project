from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import robotData
from .models import robotData2
from .models import requestData
# for timing the robotData database.
from datetime import datetime
from datetime import timedelta
import time


from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import pytz

# for ajax request.
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers
from django.http import HttpResponse

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
    rd = list(robotData2.objects.all())
    return render(
        request,
        'dashboard/databaseTable.html',
        {'rd' : rd},
    )
        
def create1data(request):
    rd = robotData2()
    rd.robotPositionY = 10
    rd.robotPositionX = 10
    rd.postime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rd.save()
    return render(
        request,
        'dashboard/databaseTable.html',
    )

# 현재시간의 데이터를 요청합니다.
# 현재 데이터가 없다면, 1초전의 데이터를 요청합니다.
def requestNowdata(request):

    '''
    t1 = datetime.now()
    t2 = t1 - timedelta(seconds=1)
    c1 = t1.strftime('%Y-%m-%d %H:%M:%S')
    c2 = t2.strftime('%Y-%m-%d %H:%M:%S')
    
    grd = robotData2.objects.get(postime=c1)
    context = {
                'grd.postime':grd.postime
            }
    return render(
           request,
           'dashboard/requestNowdata.html',
           context,
    )
    '''
    try:
        t1 = datetime.now()
        t2 = t1 - timedelta(seconds=1)
        c1 = t1.strftime('%Y-%m-%d %H:%M:%S')
        c2 = t2.strftime('%Y-%m-%d %H:%M:%S')
        
        grd = robotData2.objects.get(postime=c1)
        logs = "first database request successed. request time is " + c1 + "\n data time is " + grd.postime
        context = {
                'data_postime':str(grd.postime),
                'data_x': str(grd.robotPositionX),
                'data_y': str(grd.robotPositionY),
                'logs': logs,
                }
        return render(
            request,
            'dashboard/requestNowdata.html',
            context,
        )
    except ObjectDoesNotExist:
        logs = "\nfirst database request failed."
        try:
            grd = robotData2.objects.get(postime=c2)
            logs = "second database request successed. request time is " + c2 + "\n data time is " + grd.postime
            context = {
                'data_postime':str(grd.postime),
                'data_x': str(grd.robotPositionX),
                'data_y': str(grd.robotPositionY),
                'logs' : logs
            }
            return render(
                request,
                'dashboard/requestNowdata.html',
                context,
            )
        except ObjectDoesNotExist:
            logs += "\nsecond database request failed. "
            context = {
                'logs': logs,
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
        rd.robotPositionY = int(float(receive_message_x))
        rd.robotPositionX = int(float(receive_message_y))
        rd.checked_at = datetime.now()
        rd.save()
        send_message = {'send_data' : "I received "+ receive_message_x + " and " + receive_message_y}
        return JsonResponse(send_message)
        
# request Data of Now.
def rqDataNowJson(request):
    t1 = datetime.now()
    t2 = t1 - timedelta(seconds=1)
    c1 = t1.strftime('%Y-%m-%d %H:%M:%S')
    c2 = t2.strftime('%Y-%m-%d %H:%M:%S')
        
    grd = robotData2.objects.get(postime=c2)
    results = []
    results.append({
        "postime":grd.postime,
        "x" : grd.robotPositionX,
        "y" : grd.robotPositionY
    })
    return JsonResponse({"results":results}, status=200)
    #grd_list = serializers.serialize('json', grd)
    #return HttpResponse(grd_list, content_type="text/json-comment-filtered")
    
# request example response.
def rqDataExJson(request):
    grd = robotData2.objects.get(pk=1)
    results = []
    results.append({
        "postime":grd.postime,
        "x" : grd.robotPositionX,
        "y" : grd.robotPositionY
    })
    return JsonResponse({"results":results}, status=200)
    
def requestDelivery(request):
    if request.method == 'GET':
      if request.GET.get('requestPosition').isdigit():
        if request.GET.get('requestMethod').isdigit():
          
          requestPosition = request.GET.get('requestPosition')
          requestMethod = request.GET.get('requestMethod')
          
          # database post
          rd = requestData()
          rd.requestPosition = int(requestPosition)
          rd.requestMethod = int(requestMethod)
          rd.requestTime = datetime.now()
          rd.save()
        
          context = {
            "requestPosition": requestPosition,
            "requestMethod" : requestMethod,
            "status" : "well"
          }
          return render(request, 'dashboard/requestDeliveryResult.html', context)
          
        else :
          context = {
              "status" : "wrongRequestMethod"
            }
          return render(request, 'dashboard/requestDeliveryResult.html', context)
      else :
        context = {
              "status" : "wrongRequestPosition"
            }
        return render(request, 'dashboard/requestDeliveryResult.html', context)
    else :
      context = {
              "status" : "notGet"
            }
      return render(request, 'dashboard/requestDeliveryResult.html', context)
