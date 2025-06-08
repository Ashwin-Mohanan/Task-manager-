from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.conf import settings
import os
import json
from .models import Task
import datetime
import traceback
import requests
from django.views.decorators.csrf import csrf_exempt
import base64
# Create your views here.
def taskDashboard(request):
    task = Task.objects.all()
    tag_type = Task.objects.values_list('tag_type', flat=True).distinct()
    return render(request, 'home.html',{'task':task,'tag_type':tag_type})

def taskCreator(request):
    return render(request, 'taskCreator.html')

def fileSave(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        uploaded_files = request.FILES.getlist(id)
        # file_names = [file.name for file in uploaded_files]
        static_upload_path = os.path.join(settings.BASE_DIR,'taskmanger','static','TaskFiles')
        os.makedirs(static_upload_path, exist_ok=True)
        saved_files = []
        for f in uploaded_files:
            fname = f.name
            extention =  fname.split('.')[1]
            fname = f"{id}.{extention}"
            save_path = os.path.join(static_upload_path, fname)
            

            if os.path.exists(save_path):
                os.remove(save_path)

            with open(save_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            saved_files.append(fname)
        

        return JsonResponse({'status': 'File save succesfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def taskSave(request):
    if request.method == 'POST':
        d = request.POST.get('Data')
        file_objs = request.FILES.getlist('files')
        try:
            payload = json.loads(d)
            for task in payload:
                if task.get('tag_type') == 'select-files':
                    file_dict = {}
                    for file in file_objs:
                        if file.name in task.get('file_names', []):
                            # encodeing the file content into base64
                            encoded_content = base64.b64encode(file.read()).decode('utf-8')
                            file_dict[file.name] = {
                                'name': file.name,
                                'content': encoded_content
                            }
                    task['files'] = file_dict

            response = requests.post(
                'http://127.0.0.1:8000/ApiDetails/ApiTaskSave',
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            data = response.json()
        except Exception as e:
            data = {'error': str(e)}

        return JsonResponse(data)


def DelTask(request,id):
    response = requests.post(
            'http://127.0.0.1:8000/ApiDetails/ApiDelTask',
            data=json.dumps(id),
            headers={'Content-Type': 'application/json'}
    )
    data = response.json()
    return redirect('taskDashboard')


def openeditTask(request,id):
     
    taskSave = Task.objects.get(taskid = id)
    data={}
    data['id'] = taskSave.taskid
    data['title'] = taskSave.title
    data['description'] = taskSave.description
    data['due_date'] = taskSave.due_date
    data['tag_type'] = taskSave.tag_type
    data['tag'] = taskSave.tag
    data = [data]
    # static_upload_path = os.path.join(settings.BASE_DIR,'taskmanger','static','TaskFiles')

    return render(request, 'editTaskCreator.html', {'data': data, 'id':taskSave.taskid})

@csrf_exempt
def editSave(request):
    if request.method == 'POST':
        d = request.POST.get('Data')
        file_objs = request.FILES.getlist('files')
        try:
            payload = json.loads(d)
            for task in payload:
                if task.get('tag_type') == 'select-files':
                    file_dict = {}
                    for file in file_objs:
                        if file.name in task.get('file_names', []):
                            
                            encoded_content = base64.b64encode(file.read()).decode('utf-8')
                            file_dict[file.name] = {
                                'name': file.name,
                                'content': encoded_content
                            }
                    task['files'] = file_dict

            response = requests.post(
                'http://127.0.0.1:8000/ApiDetails/ApiTaskEditSave',
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            data = response.json()
        except Exception as e:
            data = {'error': str(e)}

        return JsonResponse(data)

