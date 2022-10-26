from django.urls import path, include
from . import views


urlpatterns = [
    path('databaseTest', views.databaseTest, name='databaseTest'),
    path('robotDataCleanUp', views.robotDataCleanUp,),
    path('updateDatabase/',views.updateDatabase),
    path('ajax_method/',views.ajax_method, name='ajax_method'),
]