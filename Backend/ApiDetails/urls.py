from django.urls import path
from ApiDetails import views
urlpatterns = [
    path('ApiTaskSave', views.ApiTaskSave, name='ApiTaskSave'),
    path('ApiTaskEditSave', views.ApiTaskEditSave, name='ApiTaskEditSave'),
    path('ApiDelTask', views.ApiDelTask, name='ApiDelTask'),
    
]