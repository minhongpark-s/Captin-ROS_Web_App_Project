from django.urls import path, include
from . import views


urlpatterns = [
    path('databaseTest', views.databaseTest, name='databaseTest'),
    
    path('robotAllDataCleanUp', views.robotDataCleanUp,),
    path('robotLatestDataCleanUp', views.robotLatestDataCleanUp,),
    path('deliveryAllDataCleanUp', views.deliveryDataCleanUp,),
    path('deliveryLatestDataCleanUp', views.deliveryDataCleanUp,),
    
    
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
    path('changeMovingToLoadingReady/', views.changeMovingToLoadingReady, name='changeMovingToLoadingReady'),
    path('requestLatestDelStatus/',views.requestLatestDelStatus, name='requestLatestDelStatus'),
    path('checkLoadedData/',views.checkLoadedData, name='checkLoadedData'),
    path('changeLoadedToMovingToUnload/', views.changeLoadedToMovingToUnload, name='changeLoadedToMovingToUnload'),
    path('changeMovingToUnloadToUnloadReady/', views.changeMovingToUnloadToUnloadReady, name='changeMovingToUnloadToUnloadReady'),
    path('changeMovingToUnloadToUnloadedandMovingToOrigin/', views.changeMovingToUnloadToUnloadedandMovingToOrigin, name='changeMovingToUnloadToUnloadedandMovingToOrigin'),
    path('loadedCheck/', views.loadedCheck , name='loadedCheck'),
    path('changeUnloadedandMovingToOriginToFinished/', views.changeUnloadedandMovingToOriginToFinished, name='changeUnloadedandMovingToOriginToFinished')
]