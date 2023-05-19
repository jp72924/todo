from django.utils import timezone


def localtime():
	now = timezone.now()
	return timezone.localtime(now)