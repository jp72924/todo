from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from . models import Task


def task_list(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks, 'form_action': 'add/'}
    return render(request, 'list/task_list.html', context)


def task_create(request):
    if request.method == 'POST':
        task = Task()
        task.title = request.POST.get('title')
        task.descrip = request.POST.get('descrip')
        task.due_date = request.POST.get('due-date') or timezone.now()
        if 'important' in request.POST:
            task.important = True
        task.save()

    return redirect('task_list')


def task_mark(request, id):
    task = get_object_or_404(Task, id=id)
    task.status = Task.Status.SUCCESS
    task.save()

    return redirect('task_list')


def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()

    return redirect('task_list')
