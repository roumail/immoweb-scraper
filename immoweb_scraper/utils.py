import datetime


def get_current_time_str() -> str:
    today_date = datetime.datetime.today()
    return today_date.strftime("%Y-%m-%d-%H:%M:%S")
