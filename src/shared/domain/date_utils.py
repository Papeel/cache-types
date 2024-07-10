import datetime


class DateUtils:
    @staticmethod
    def utc_now() -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)
