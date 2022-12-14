from http.client import HTTPResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

import math

from .models import robotData
from .models import robotData2
from .models import requestData
from .models import requestDelData
# for timing the robotData database.
from datetime import datetime
from datetime import timedelta
import time

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import pytz

# for ajax request.
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers
from django.http import HttpResponse

def robotDataCleanUp(request):
    q = robotData2.objects.all()
    q.delete()
    return redirect('showAllDatabases')

def robotLatestDataCleanUp(request):
    q = robotData2.objects.all().latest('requestTime')
    q.delete()
    return redirect('showAllDatabases')
    
def deliveryDataCleanUp(request):
    q = requestDelData.objects.all()
    q.delete()
    return redirect('showAllDatabases')

def deliveryLatestDataCleanUp(request):
    q = requestDelData.objects.all().latest('requestTime')
    q.delete()
    return redirect('showAllDatabases')

def databaseTest(request):
    return render(
        request,
        'dashboard/databaseTest.html',
    )

@csrf_exempt
def updateDatabase(request):
    if request.method == 'GET':
        rd = robotData2()
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
    rdd = list(requestDelData.objects.all())
    return render(
        request,
        'dashboard/databaseTable.html',
        {'rd' : rd,'rdd' : rdd },
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
def requestNowData(request):

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
        except MultipleObjectsReturned:
            logs = "second request, two data arrived."
            grd = robotData2.objects.filter(postime=c2).first()
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
    except robotData2.MultipleObjectsReturned:
        logs = "first requset, two data arrived."
        grd = robotData2.objects.filter(postime=c1).first()
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
def dataconnection(request):
    if request.method == 'POST':
        scalingFactor = 10
        receive_message_x = request.POST.get('x')
        receive_message_y = request.POST.get('y')
        dn = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        rd = robotData2()
        cvX = int(float(receive_message_x)*scalingFactor)
        cvY = int(float(receive_message_y)*scalingFactor)
        rd.robotPositionX = cvX
        rd.robotPositionY = cvY
        rd.postime = dn
        rd.save()
        send_message = {
          'server received': 'x '+receive_message_x+ ', y: ' + receive_message_y,
          'server database saved': 'x: '+ str(cvX) + ", y: " + str(cvY) + ", time: " + dn ,
          'scalingFactor':scalingFactor}
        return JsonResponse(send_message)
        
# request Data of Now.
'''
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
'''
def rqNowDataJson(request):
    try:
        t1 = datetime.now()
        t2 = t1 - timedelta(seconds=1)
        c1 = t1.strftime('%Y-%m-%d %H:%M:%S')
        c2 = t2.strftime('%Y-%m-%d %H:%M:%S')
        
        grd = robotData2.objects.get(postime=c1)
        check = requestDelData.objects.all().latest('requestTime')
        if check.referenceStatus == "Unloaded, Moving To Origin":
          status = "True"
        else:
          status = "False"
        results = []
        results.append({
            "postime":grd.postime,
            "x" : Scaling(grd.robotPositionX/10*1.5),
            "y" : Scaling(grd.robotPositionY/10*1.5),
            "endStatus": status
        })
        return JsonResponse({"results":results}, status=200)
    except ObjectDoesNotExist:
        logs = "\nfirst database request failed."
        try:
            grd = robotData2.objects.get(postime=c2)
            check = requestDelData.objects.all().latest('requestTime')
            if check.referenceStatus == "Unloaded, Moving To Origin":
              status = "True"
            else:
              status = "False"
            results = []
            results.append({
                "postime":grd.postime,
                "x" : Scaling(grd.robotPositionX/10*1.5),
                "y" : Scaling(grd.robotPositionY/10*1.5),
                "endStatus": status
            })
            return JsonResponse({"results":results}, status=200)
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
        except MultipleObjectsReturned:
            logs = "second request, two data arrived."
            grd = robotData2.objects.filter(postime=c2).first()
            results = []
            results.append({
                "postime":grd.postime,
                "x" : Scaling(grd.robotPositionX/10*1.5),
                "y" : Scaling(grd.robotPositionY/10*1.5)
            })
            return JsonResponse({"results":results}, status=200)
    except robotData2.MultipleObjectsReturned:
        logs = "first requset, two data arrived."
        grd = robotData2.objects.filter(postime=c1).first()
        results = []
        results.append({
            "postime":grd.postime,
            "x" : Scaling(grd.robotPositionX/10*1.5),
            "y" : Scaling(grd.robotPositionY/10*1.5)
        })
        return JsonResponse({"results":results}, status=200)

    
# request example response.
def rqExDataJson(request):
    #grd = robotData2.objects.get(pk=1)
    tx = 102
    rx = 90
    results = []
    results.append({
        "postime":grd.postime,
        #"x" : grd.robotPositionX,
        #"y" : grd.robotPositionY,
        "x" : tx/10
    })
    return JsonResponse({"results":results}, status=200)

def Scaling(num):
  if num%math.floor(num) >= 0.75:
    result = math.floor(num)+1
  if(num%math.floor(num) < 0.75): 
    if(num%math.floor(num) >= 0.25):
      result = math.floor(num)+0.5
  if num%math.floor(num) < 0.25:
    result = math.floor(num)
  return result
    
    
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
      
# 앱에서 배송받는 사람이 주소지와 배송방법을 선택하고 배송시작을 누르면 실행되는 함수.
def requestDeliveryJsonResponse(request):
    if request.method == 'GET':
      if request.GET.get('requestPosition').isdigit():
        if request.GET.get('requestMethod').isdigit():
          requestPosition = request.GET.get('requestPosition')
          requestMethod = request.GET.get('requestMethod')
          
          # 현재시간을 문자열로 변환후 저장.
          NT = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
          
          # database에 데이터를 저장.
          rd = requestDelData()
          rd.requestPosition = int(requestPosition)
          rd.requestMethod = int(requestMethod)
          rd.requestTime = NT
          rd.referenceStatus = "False"
          rd.save()
          
          # 로봇상태가 moving일 경우 즉시 Moving을 return후 종료.
          if(requestDelData.objects.filter(Q(referenceStatus="Moving")|Q(referenceStatus="Loading Ready")|Q(referenceStatus="loaded")|Q(referenceStatus="Moving To Unload")|Q(referenceStatus="Unloaded, Moving To Origin")).count() > 0):
            rg = requestDelData.objects.get(requestTime=NT)
            if rg.referenceStatus == "False":
              rg.delete()
            results = []
            results.append({
                  "status" : "rejected because robot is delivering.",
            })
            return JsonResponse({"results":results}, status=200)
          i = 0
          # 로봇상태가 moving이 아닌 경우while문을 실행.
          while(1):
            # 매 반복마다 데이터베이스를 새로 불러옴.
            grd = requestDelData.objects.get(requestTime=NT)
            # 기존의 referenceStatus가 False에서 Moving으로 바뀌면 ok를 return후 종료.
            if grd.referenceStatus == "Moving":
              results = []
              results.append({
                  "requestPosition": requestPosition,
                  "requestMethod" : requestMethod,
                  "status" : "ok"
              })
              return JsonResponse({"results":results}, status=200)
            # 5초 반복후 referenceStatus의 변화가 없으면 timeout을 return후 종료.
            if i > 20:
              grd.delete()
              results = []
              results.append({
                  "requestPosition": requestPosition,
                  "requestMethod" : requestMethod,
                  "status" : "timeout"
              })
              return JsonResponse({"results":results}, status=200)
            time.sleep(1)
            i = i + 1
            
# 앱에서 배송자가 적재완료 버튼을 누르면 실행되는 함수.
# app's request   
def shippedCheck(request):
    if request.method == 'GET':
      DN=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      # shippedStatus를 확인후 True일 경우 True를 return
      shippedStatus = request.GET.get('shippedStatus')
      if shippedStatus == "True":
        ########################################################## 기능 구현 필요. 로봇에 데이터 전송. ########################################################
        try:
          grd = requestDelData.objects.get(referenceStatus="Loading Ready")
          grd.referenceStatus = "Loaded"
          grd.loadedTime = DN
          grd.save()
          results = []
          results.append({
            "status" : "changed 'Loading Ready' to 'Loaded'",
            "nowTime": DN,
              })
          return JsonResponse({"response1":results}, status=200)
        except ObjectDoesNotExist:
          results = []
          results.append({
            "status" : "no 'Loading Ready' request.",
            "nowTime": DN,
              })
          return JsonResponse({"response1":results}, status=200)
        #######################################################################################################################################################
        results = []
        results.append({
            "shippedStatus": "True"
        })
        return JsonResponse({"results":results}, status=200)
      else:
        results = []
        results.append({
            "shippedStatus": "False"
        })
        return JsonResponse({"results":results}, status=200)

# 로봇에서 주기적으로 데이터베이스 조회할때 쓰는 함수.   
def newestRefCheck(request):
    if request.method == 'GET':
      try:
        grd = requestDelData.objects.filter(referenceStatus="Moving").latest('requestTime')
        '''
        results = []
        results.append({
            "status" : "something wrong",
        })
        return JsonResponse({"results":results}, status=200)
        '''
        
        grd.referenceStatus = "Moving"
        DN=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        grd.referenceTime = DN
        grd.save()
        results = []
        results.append({
            "status" : "find newest reference False data completed. fix to Moving completed.",
            "referenceTime": DN,
            "position" : grd.requestPosition,
            "method" : grd.requestMethod,
        })
        return JsonResponse({"results":results}, status=200)
      except ObjectDoesNotExist:
        DN=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        results = []
        results.append({
            "status" : "find newest reference False data failed.",
            "nowTime": DN,
        })
        return JsonResponse({"results":results}, status=200)
        
# 로봇에서 주기적으로 데이터베이스 조회할때 쓰는 함수.        
def checkDeliveryRequest(request):
    if request.method == 'GET':
        DN=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            grd = requestDelData.objects.filter(referenceStatus="False").latest('requestTime')
            # 데이터베이스 수정
            #grd.referenceStatus="Moving"
            #grd.referenceTime=DN
            #grd.save()
            # 데이터베이스 참조
            position = grd.requestPosition
            method = grd.requestMethod
            
            results = []
            results.append({
                "status" : "found request",
                "nowTime": DN,
                "position": position,
                "method": method,
            })
            return JsonResponse({"response1":results}, status=200)
            
        except ObjectDoesNotExist:
            results = []
            results.append({
                "status" : "no request",
                "nowTime": DN,
            })
            return JsonResponse({"response1":results}, status=200)
            
def checkLoadedData(request):
    if request.method == 'GET':
      DN=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      try:
        grd = requestDelData.objects.get(referenceStatus="Loaded")
        results = []
        results.append({
          "status" : "found Loaded Data",
          "nowTime": DN,
        })
        return JsonResponse({"response1":results}, status=200)
      except ObjectDoesNotExist:
        results = []
        results.append({
          "status" : "no Loaded Data",
          "nowTime": DN,
        })
        return JsonResponse({"response1":results}, status=200)
def changeFalseToMoving(request):
    if request.method == 'GET':
      #DN = request.GET.get('requestTime')
      try:
        #grd = requestDelData.objects.get(requestTime=DN)
        grd = requestDelData.objects.all().latest('requestTime')
        grd.referenceStatus = "Moving"
        grd.MSTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        grd.save()
        results = []
        results.append({
          "status" : "False changed to Moving.",
          "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        return JsonResponse({"response1":results}, status=200)
      except ObjectDoesNotExist:
            results = []
            results.append({
                "status" : "no database exist",
                "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
            return JsonResponse({"response1":results}, status=200)
            
def changeMovingToLoadingReady(request):
    if request.method == 'GET':
      #DN = request.GET.get('requestTime')
      try:
        grd = requestDelData.objects.get(referenceStatus="Moving")
        grd.referenceStatus = "Loading Ready"
        grd.loadingReadyTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        grd.save()
        results = []
        results.append({
          "status" : "'Moving' changed to 'Loading Ready'.",
          "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        return JsonResponse({"response1":results}, status=200)
      except ObjectDoesNotExist:
            results = []
            results.append({
                "status" : "no moving data found",
                "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
            return JsonResponse({"response1":results}, status=200)
      
def changeLoadedToMovingToUnload(request):
    if request.method == 'GET':
      #DN = request.GET.get('requestTime')
      try:
        grd = requestDelData.objects.get(referenceStatus="Loaded")
        grd.referenceStatus = "Moving To Unload"
        grd.MTUTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        grd.save()
        results = []
        results.append({
          "status" : "'Loaded' changed to  'Moving To Unload.",
          "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        return JsonResponse({"response1":results}, status=200)
      except ObjectDoesNotExist:
            results = []
            results.append({
                "status" : "no Loaded data found",
                "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
            return JsonResponse({"response1":results}, status=200)

# robot이 status 3을 publish하면 실행되는 함수.
# robot's request            
def changeMovingToUnloadToUnloadReady(request):
    if request.method == 'GET':
      #DN = request.GET.get('requestTime')
      try:
        grd = requestDelData.objects.get(referenceStatus="Moving To Unload")
        grd.referenceStatus = "Unload Ready"
        grd.URTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        grd.save()
        results = []
        results.append({
          "status" : "'Moving To Unload' changed to 'Unload Ready.",
          "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        return JsonResponse({"response1":results}, status=200)
      except ObjectDoesNotExist:
            results = []
            results.append({
                "status" : "no Moving To Unload data found",
                "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
            return JsonResponse({"response1":results}, status=200)
            
# robot이 status 3을 publish하면 실행되는 함수.
# robot's request            
def changeMovingToUnloadToUnloadedandMovingToOrigin(request):
    if request.method == 'GET':
      #DN = request.GET.get('requestTime')
      try:
        grd = requestDelData.objects.get(referenceStatus="Moving To Unload")
        grd.referenceStatus = "Unloaded, Moving To Origin"
        grd.UMTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        grd.save()
        results = []
        results.append({
          "status" : "'Moving To Unload' changed to 'Unloaded, Moving To Origin.",
          "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        return JsonResponse({"response1":results}, status=200)
      except ObjectDoesNotExist:
            results = []
            results.append({
                "status" : "no Moving To Unload data found",
                "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
            return JsonResponse({"response1":results}, status=200)

# 앱에서 배송자가 수령완료 버튼을 누르면 실행되는 함수.     
# app's request   
def loadedCheck(request):
    if request.method == 'GET':
      DN=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      # loadedStatus를 확인후 True일 경우 True를 return
      loadedStatus = request.GET.get('loadedStatus')
      if loadedStatus == "True":
        ########################################################## 로봇에 데이터 전송. ########################################################
        try:
          grd = requestDelData.objects.get(referenceStatus="Unload Ready")
          grd.referenceStatus = "Delivery Received"
          grd.DRTime = DN
          grd.save()
          results = []
          results.append({
            "status" : "changed 'Unload Ready' to 'Delivery Received'",
            "nowTime": DN,
              })
          return JsonResponse({"response1":results}, status=200)
        except ObjectDoesNotExist:
          results = []
          results.append({
            "status" : "no 'Unload Ready' request.",
            "nowTime": DN,
              })
          return JsonResponse({"response1":results}, status=200)
        #######################################################################################################################################################
        results = []
        results.append({
            "shippedStatus": "True"
        })
        return JsonResponse({"results":results}, status=200)
      else:
        results = []
        results.append({
            "loadedStatus": "False"
        })
        return JsonResponse({"results":results}, status=200)
        
        
def changeUnloadedandMovingToOriginToFinished(request):
    if request.method == 'GET':
      #DN = request.GET.get('requestTime')
      try:
        grd = requestDelData.objects.get(referenceStatus="Unloaded, Moving To Origin")
        grd.referenceStatus = "Finished"
        grd.FTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        grd.save()
        results = []
        results.append({
          "status" : "'Unloaded, Moving To Origin' changed to 'Finished.",
          "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        return JsonResponse({"response1":results}, status=200)
      except ObjectDoesNotExist:
            results = []
            results.append({
                "status" : "no 'Unloaded, Moving To Origin' data found",
                "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
            return JsonResponse({"response1":results}, status=200)
            
def requestLatestDelStatus(request):
    if request.method == 'GET':
      DN=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      try:
        grd = requestDelData.objects.latest('requestTime')
        results = []
        results.append({
          "status" : "'Moving' changed to 'Loading Ready'.",
          "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          "Status" : grd.referenceStatus
        })
        return JsonResponse({"response1":results}, status=200)
      except ObjectDoesNotExist:
            results = []
            results.append({
                "status" : "no data found",
                "nowTime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
            return JsonResponse({"response1":results}, status=200) 