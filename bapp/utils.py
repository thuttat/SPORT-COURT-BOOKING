import datetime


def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def calculate_duration(start_time, end_time):
    dummy_date = datetime.datetime.today()
    dt_start = datetime.datetime.combine(dummy_date, start_time)
    dt_end = datetime.datetime.combine(dummy_date, end_time)
    return (dt_end - dt_start).total_seconds() / 3600.0

