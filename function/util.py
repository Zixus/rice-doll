from datetime import timedelta

LOCAL_OFFSET_HOUR = 7
TIME_FORMAT = "%d-%m-%Y, %H:%M"


def get_local_timestamp(ts):
    local_ts = ts + timedelta(hours=LOCAL_OFFSET_HOUR)
    return local_ts.strftime(TIME_FORMAT)
