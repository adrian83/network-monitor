
from datetime import datetime

import speedtest
import sys

from .models import Metrics

mega_byte = 1024 * 1024

def measure_speed():
    print("test")
    try:
        print("starting")
        d_speed = 0
        u_speed = 0
        d_error = None
        u_error = None
        date = datetime.now()

        s = None

        try:
            s = speedtest.Speedtest()
        except:
            d_error = sys.exc_info()[0]
            u_error = d_error
            print("Error : {0}".format(d_error))

        if s:
            try:
                print("2")
                d_speed = s.download() / mega_byte
            except:
                d_error = sys.exc_info()[0]
                print("Error : {0}".format(d_error))

            try:
                u_speed = s.upload() / mega_byte
            except:
                u_error = sys.exc_info()[0]
                print("Error: {0}".format(u_error))

        m = Metrics(
            download_speed=d_speed,
            download_error=d_error,
            upload_speed=u_speed,
            upload_error=u_error,
            date=date)

        m.save()

        print("storing: {0}".format(m))
    except Exception as e:
        print("Error: {0}".format(e))
