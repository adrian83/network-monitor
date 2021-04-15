from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.core import serializers
from django.template import loader
from django.utils.timezone import make_aware


from datetime import datetime, timedelta

from .models import Metrics

datetime_tmpt = '%Y.%m.%d_%H:%M:%S'

template = loader.get_template('network/index.html')

d_speed = lambda m : m.download_speed
d_error = lambda m : m.download_error
u_speed = lambda m : m.upload_speed
u_error = lambda m : m.upload_error



def to_datetime(dt_str):
    if not dt_str:
        return None

    try:
        return make_aware(datetime.strptime(dt_str, datetime_tmpt))
    except: # ValueError as ve:
        return None


def to_string(dt):
    return dt.strftime(datetime_tmpt)

class Error:

    def __init__(self, date, msg):
        self.date = date
        self.message = msg


class Stats:

    def __init__(self, max_speed, min_speed, avg_speed, count, errors):
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.avg_speed = avg_speed
        self.count = count
        self.errors = errors
        self.max_speed_prct = 100 if max_speed > 0 else 0
        self.min_speed_prct = int((min_speed / max_speed) * 100) if max_speed > 0 else 0
        self.avg_speed_prct = int((avg_speed / max_speed) * 100) if max_speed > 0 else 0

def stats_from_metrics(metrics, get_speed, error_msg):
    if not metrics:
        return Stats(0, 0, 0, 0, [])

    min_speed = get_speed(metrics[0])
    max_speed = get_speed(metrics[0])
    speed_sum = 0
    count = 0
    errors = []

    for m in metrics:
        msg = error_msg(m)
        if msg:
            errors.append(Error(m.date, msg))
            continue

        speed = get_speed(m)
        max_speed = speed if speed > max_speed else max_speed
        min_speed = speed if speed < min_speed else min_speed
        speed_sum += speed
        count += 1

    errors.sort(key=lambda e: e.date, reverse=True)

    avg_speed = speed_sum / count if count else 0

    return Stats(max_speed, min_speed, avg_speed, count, errors)

class Result:
    def __init__(self, download_stats, upload_stats, metrics):
        self.download_stats = download_stats
        self.upload_stats = upload_stats
        self.metrics = metrics

class MetricsView(View):

    def get(self, request, *args, **kwargs):

        from_str = request.GET.get("from_hours")
        if not from_str:
            return redirect('/?from_hours={0}'.format(4))


        hours = int(from_str)
        from_dt = make_aware(datetime.now()) - timedelta(hours=hours, minutes=0)

        metrics = Metrics.objects.filter(date__gt=from_dt) #, date__lt=to_dt)

        d_stats = stats_from_metrics(metrics, d_speed, d_error)
        u_stats = stats_from_metrics(metrics, u_speed, u_error)

        result = Result(d_stats, u_stats, metrics)

        context = {'result': result}
        return HttpResponse(template.render(context, request))
