from datetime import timedelta, datetime


def compute_average_time(timestamps):
    if not timestamps:
        return None
    total_seconds = sum(t.hour * 3600 + t.minute * 60 + t.second for t in timestamps)
    avg_seconds = total_seconds // len(timestamps)
    avg_time = timedelta(seconds=avg_seconds)
    return (datetime.min + avg_time).time()  # Convert to time object