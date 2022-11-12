from django.urls import path, include
from . import views


urlpatterns = [
    path('databaseTest', views.databaseTest, name='databaseTest'),
    path('robotDataCleanUp', views.robotDataCleanUp,),
    path('updateDatabase/',views.updateDatabase),
    path('ajax_method/',views.ajax_method, name='ajax_method'),
    path('showAllDatabases/',views.showAllDatabases, name='showAllDatabases'),
    path('create1data/', views.create1data, name='create1data'),
    path('requestNowdata/', views.requestNowdata, name='requestNowdata'),

    path('dataconnection', views.dataconnection, name='dataconnection'),
    
    path('rqDataNowJson/', views.rqDataNowJson, name='rqDataNowJson'),
    path('rqDataExJson/', views.rqDataExJson, name='rqDataExJson'),
]