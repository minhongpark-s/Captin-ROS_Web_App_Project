from django.urls import path, include
from . import views


urlpatterns = [
    path('databaseTest', views.databaseTest, name='databaseTest'),
    path('robotDataCleanUp', views.robotDataCleanUp,),
    path('deliveryDataCleanUp', views.deliveryDataCleanUp,),
    path('updateDatabase/',views.updateDatabase),
    path('ajax_method/',views.ajax_method, name='ajax_method'),
    path('showAllDatabases/',views.showAllDatabases, name='showAllDatabases'),
    path('create1data/', views.create1data, name='create1data'),
    path('requestNowData/', views.requestNowData, name='requestNowData'),

    path('dataconnection', views.dataconnection, name='dataconnection'),
    
    path('rqNowDataJson/', views.rqNowDataJson, name='rqNowDataJson'),
    path('rqExDataJson/', views.rqExDataJson, name='rqExDataJson'),
    path('requestDelivery/', views.requestDelivery, name='requestDelivery'),
    path('requestDeliveryJsonResponse/', views.requestDeliveryJsonResponse, name='requestDeliveryJsonResponse'),
    path('shippedCheck/', views.shippedCheck, name='shippedCheck'),
    path('newestRefCheck/', views.newestRefCheck, name='newestRefCheck'),
    path('checkDeliveryRequest/', views.checkDeliveryRequest, name='checkDeliveryRequest'),
    path('changeFalseToMoving/', views.changeFalseToMoving, name='changeFalseToMoving'),
    path('changeMovingToEnd/', views.changeMovingToEnd, name='changeMovingToEnd'),
]