from django.utils.timezone import make_aware

from datetime import datetime

import speedtest
import sys

from .models import Metrics

mega_byte = 1024 * 1024

def measure_speed():
    try:
        d_speed = 0
        u_speed = 0
        d_error = None
        u_error = None
        date = make_aware(datetime.now())

        s = None

        try:
            s = speedtest.Speedtest()
        except ValueError as e:
            error = str(e)
            u_error = error
            d_error = error
        except speedtest.ConfigRetrievalError as e:
            error = "no internet access or unavailable config: ({0})".format(str(e))
            u_error = error
            d_error = error
        except:
            error = "unknown error: ({0})".format(str(sys.exc_info()[0]))
            u_error = error
            d_error = error

        if s:
            try:
                d_speed = s.download() / mega_byte
            except:
                d_error = "unknown error: ({0})".format(str(sys.exc_info()[0]))

            try:
                u_speed = s.upload() / mega_byte
            except:
                u_error = "unknown error: ({0})".format(str(sys.exc_info()[0]))

        m = Metrics(
            download_speed=d_speed,
            download_error=d_error,
            upload_speed=u_speed,
            upload_error=u_error,
            date=date)

        m.save()

        print("storing: {0}".format(m))
    except Exception as e:
        print("error: {0}".format(e))
