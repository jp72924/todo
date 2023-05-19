from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from . models import Task


def task_list(request):
    all_tasks = Task.pending.all()
    tasks_overdue = [task for task in all_tasks if task.is_overdue()]
    tasks_pending = list(set(all_tasks) - set(tasks_overdue))
    context = {'overdue': tasks_overdue, 'pending': tasks_pending, 'form_action': 'add/'}
    return render(request, 'list/task_list.html', context)


def task_create(request):
    if request.method == 'POST':
        now = timezone.now()
        local_time = timezone.localtime(now)

        task = Task()
        task.title = request.POST.get('title')
        task.descrip = request.POST.get('descrip')
        task.due_date = request.POST.get('due-date') or local_time.date()
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
