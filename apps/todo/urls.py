from django.urls import path
from .views import TodosView,TodoDetailsview,TasksView,TaskDetailsView


urlpatterns = [
    path('todos', TodosView.as_view()),
    path("todos/<int:todo_id>", TodoDetailsview.as_view()),
    path("todos/<int:todo_id>/tasks",TasksView.as_view()),
    path("todos/<int:todo_id>/task/<int:task_id>",TaskDetailsView.as_view()),
]
