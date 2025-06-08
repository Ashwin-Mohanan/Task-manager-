from django.urls import path
from taskmanger import views
urlpatterns = [
    path('', views.taskDashboard, name='taskDashboard'),
    path('taskSave', views.taskSave, name='taskSave'),
    path('taskCreator', views.taskCreator, name = 'taskCreator'),
    path('fileSave', views.fileSave, name = 'filesave'),
    path('DelTask/<str:id>/',views.DelTask,name='DelTask'),
    path('openeditTask/<str:id>/',views.openeditTask,name='openeditTask'),
    path('editSave',views.editSave,name='editSave'),


]