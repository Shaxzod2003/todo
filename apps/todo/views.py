from django.http import HttpRequest, JsonResponse
from django.views import View
from django.forms import model_to_dict
from .models import Todo,Task
from django.contrib.auth.models import User
import json
from base64 import b64decode
from django.contrib.auth import authenticate
class TodosView(View):
    def get(self, request: HttpRequest) -> HttpRequest:
        header=request.headers
        auth=header["Authorization"][6:]
        username, password=b64decode(auth).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({"error":"unauthorized."},status=401)
        todos=Todo.objects.filter(user=user)
        result = []
        for todo in todos:
            result.append(model_to_dict(todo))
        
        return JsonResponse(result, safe=False)
     
    def post(self, request: HttpRequest):
        header=request.headers
        auth=header["Authorization"][6:]
        username, password=b64decode(auth).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({"error":"unauthorized."},status=401)
        
        data = json.loads(request.body.decode())

        Todo.objects.create(
            title=data.get('title'),
            user=user,
        )

        return JsonResponse({"message": "Created"})
class TodoDetailsview(View):
    def put(self, request: HttpRequest, todo_id: int):
        header=request.headers
        auth=header["Authorization"][6:]
        username, password=b64decode(auth).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({"error":"unauthorized."},status=401)
        todo=Todo.objects.get(user=user,id=todo_id)
        
        data = json.loads(request.body.decode())
        todo.title = data.get('title', todo.title)
        todo.save()

        return JsonResponse({"message": "Updated"})

    def delete(self, request: HttpRequest, todo_id: int):
        header=request.headers
        auth=header["Authorization"][6:]
        username, password=b64decode(auth).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({"error":"unauthorized."},status=401)
        todo=Todo.objects.get(user=user,id=todo_id)
        todo.delete()

        return JsonResponse({"message": "Deleted"})


class TasksView(View):
    def get(self, request: HttpRequest,  todo_id: int):
        header=request.headers
        auth=header["Authorization"][6:]
        username, password=b64decode(auth).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({"error":"unauthorized."},status=401)
        try:
            todo=Todo.objects.get(user=user,id=todo_id)
        except Todo.DoesNotExist:
            return JsonResponse({"error":"Todo does not exist"})
        tasks = Task.objects.filter(todo=todo)
        result = []
        for task in tasks:
            result.append(model_to_dict(task))

        return JsonResponse(result, safe=False)

    def post(self, request: HttpRequest, todo_id: int):
        header=request.headers
        auth=header["Authorization"][6:]
        username, password=b64decode(auth).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({"error":"unauthorized."},status=401)
        try:
            todo=Todo.objects.get(user=user,id=todo_id)
        except Todo.DoesNotExist:
            return JsonResponse({"error":"Todo does not exist"})
        data = json.loads(request.body.decode())

        Task.objects.create(
            title=data.get('title'),
            description=data.get("description"),
            todo=todo,
        )

        return JsonResponse({"message": "Created"})
class TaskDetailsView(View):
    def put(self, request: HttpRequest, todo_id: int, task_id: int):
        header=request.headers
        auth=header["Authorization"][6:]
        username, password=b64decode(auth).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({"error":"unauthorized."},status=401)
        try:
            todo=Todo.objects.get(user=user,id=todo_id)
            task=Task.objects.get(id=task_id,todo=todo)
        except (Todo.DoesNotExist, Task.DoesNotExist):
            return JsonResponse({"error":"Todo does not exist or task does not exist"})

        data = json.loads(request.body.decode())
        task.title = data.get('title', task.title)
        task.description=data.get("Description",task.description)
        task.save()

        return JsonResponse({"message": "Updated"})

    def delete(self, request: HttpRequest, todo_id: int, task_id: int):
        header=request.headers
        auth=header["Authorization"][6:]
        username, password=b64decode(auth).decode().split(":")
        user=authenticate(username=username,password=password)
        if user is None:
            return JsonResponse({"error":"unauthorized."},status=401)
        try:
            todo=Todo.objects.get(user=user,id=todo_id)
            task=Task.objects.get(id=task_id,todo=todo)
        except (Todo.DoesNotExist, Task.DoesNotExist):
            return JsonResponse({"error":"Todo does not exist or task does not exist"})
        task.delete()

        return JsonResponse({"message": "Deleted"})
    