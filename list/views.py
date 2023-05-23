from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from .utils import localtime
from .models import Task

from datetime import datetime


def task_list(request):
    now = localtime()
    tasks_overdue = Task.pending.filter(end_date__lt=now).order_by('-important', '-end_date')
    tasks_pending = Task.pending.filter(end_date__gte=now).order_by('-important')
    context = {'overdue': tasks_overdue, 'pending': tasks_pending, 'form_action': 'add/'}
    return render(request, 'list/task_list.html', context)


def task_create(request):
    now = localtime()
    if request.method == 'POST':
        task = Task()
        task.title = request.POST.get('title')
        task.descrip = request.POST.get('descrip')

        end_date = request.POST.get('end-date')
        end_time = request.POST.get('end-time')
        
        date_str = "{} {}".format(end_date, end_time)
        date_fmt = "%Y-%m-%d %H:%M"
        date_obj = datetime.strptime(date_str, date_fmt)

        task.end_date = date_obj or now.date()
        if 'important' in request.POST:
            task.important = True
        task.save()

    return redirect('task_list')


def task_toggle(request, id):
    task = get_object_or_404(Task, id=id)
    if task.status == Task.Status.SUCCESS:
        task.status = Task.Status.PENDING
    else:
        task.status = Task.Status.SUCCESS
    task.save()

    return redirect('task_list')


def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()

    return redirect('task_list')
