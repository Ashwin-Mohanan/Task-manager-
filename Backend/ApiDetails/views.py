from django.shortcuts import render
from taskmanger.models import Task
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.http import JsonResponse
import traceback
from django.conf import settings
import os
import base64
# Create your views here.
@csrf_exempt
def ApiDelTask(request):
    id = json.loads(request.body)
    taskSave = Task.objects.get(taskid = id).delete()
    data={'success':'Deleted Successfully'}
    return JsonResponse(data)



@csrf_exempt
def ApiTaskSave(request):
    try:
        dict_vals = json.loads(request.body)
        for dic in dict_vals:
            taskSave = Task()
            taskSave.title = dic['title']
            taskSave.description = dic['description']
            taskSave.due_date = dic['due_date']
            taskSave.tag_type = dic['tag_type']
            taskSave.created_at = datetime.datetime.now()
            taskSave.save()
            if dic['tag_type'] == 'select-files' and 'files' in dic:
                for original_name, file_info in dic['files'].items():
                    ext = original_name.split('.')[-1]
                    fname = f"{original_name.rsplit('.', 1)[0]}_{taskSave.taskid}.{ext}"
                    static_upload_path = os.path.join(settings.BASE_DIR, 'taskmanger', 'static', 'TaskFiles')
                    os.makedirs(static_upload_path, exist_ok=True)
                    save_path = os.path.join(static_upload_path, fname)

                    if os.path.exists(save_path):
                        os.remove(save_path)

                    # Decode base64 content and save
                    file_data = base64.b64decode(file_info['content'])
                    with open(save_path, 'wb') as destination:
                        destination.write(file_data)

                    taskSave.tag = fname
            else:
                taskSave.tag = dic.get('tag', dic['tag'])

            taskSave.save()

        data = {'Succeass': 'Successfully saved'}
    except Exception as e:
        data = {'Succeass': 'might caught some issue', 'error': str(e)}

    return JsonResponse(data)

@csrf_exempt
def ApiTaskEditSave(request):
    try:
        dict_vals = json.loads(request.body)
        
        for dic in dict_vals:
            taskSave = Task.objects.get(taskid = dic['id'])
            taskSave.title = dic['title']
            taskSave.description = dic['description']
            taskSave.due_date = dic['due_date']
            taskSave.tag_type = dic['tag_type']
            taskSave.created_at = datetime.datetime.now()
            
            if dic['tag_type'] == 'select-files' and 'files' in dic:
                for original_name, file_info in dic['files'].items():
                    ext = original_name.split('.')[-1]
                    fname = f"{original_name.rsplit('.', 1)[0]}_{taskSave.taskid}.{ext}"
                    static_upload_path = os.path.join(settings.BASE_DIR, 'taskmanger', 'static', 'TaskFiles')
                    os.makedirs(static_upload_path, exist_ok=True)
                    save_path = os.path.join(static_upload_path, fname)

                    if os.path.exists(save_path):
                        os.remove(save_path)

                    # Decode base64 content and save
                    file_data = base64.b64decode(file_info['content'])
                    with open(save_path, 'wb') as destination:
                        destination.write(file_data)

                    taskSave.tag = fname
            else:
                taskSave.tag = dic.get('tag', dic['tag'])

            taskSave.save()

        data = {'Succeass': 'Successfully saved'}
    except Exception as e:
        data = {'Succeass': 'might caught some issue', 'error': str(e)}

    return JsonResponse(data)

