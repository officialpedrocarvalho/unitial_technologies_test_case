from datetime import timedelta, datetime


def compute_average_time(timestamps):
    if not timestamps:
        return None
    total_seconds = sum(t.hour * 3600 + t.minute * 60 + t.second for t in timestamps)
    avg_seconds = total_seconds // len(timestamps)
    avg_time = timedelta(seconds=avg_seconds)
    return (datetime.min + avg_time).time()


def split_entries_by_day(data_entries):
    days = {}
    for entry in data_entries:
        timestamp = datetime.fromtimestamp(entry['timestamp'] / 1000.0)
        date_key = timestamp.date()

        if date_key not in days:
            days[date_key] = []
        days[date_key].append(entry)

    return list(days.values())


def calculate_daily_seconds(daily_entries):
    if len(daily_entries) < 2:
        return 0

    daily_entries.sort(key=lambda x: x['timestamp'])

    first_timestamp = datetime.fromtimestamp(daily_entries[0]['timestamp'] / 1000.0)
    last_timestamp = datetime.fromtimestamp(daily_entries[-1]['timestamp'] / 1000.0)
    daily_work_time = last_timestamp - first_timestamp

    return daily_work_time.total_seconds()
