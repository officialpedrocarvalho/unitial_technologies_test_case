from abc import abstractmethod, ABCMeta
from datetime import datetime, timedelta

from django.db import models
from django.db.models.base import ModelBase

from data_analyzer import utils


class MachineMeta(ABCMeta, ModelBase):
    pass


class Machine(models.Model, metaclass=MachineMeta):
    machine_id = models.CharField(max_length=255, unique=True)
    manufacturer = models.CharField(max_length=255)
    type = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def hours_worked(self, data_entries):
        """
        Calculate the total number of hours the machine has worked, grouped by day.
        """
        if not data_entries:
            return 0

        daily_entries = self.split_entries_by_day(data_entries)

        return round(sum(self.__calculate_daily_seconds(entries) for entries in daily_entries) / 3600)

    def average_start_end_time(self, data_entries):
        """
        Computes the average start and end of a machine's work, grouped by day.
        """
        days_entries = self.split_entries_by_day(data_entries)

        start_times = []
        end_times = []
        for day_entries in days_entries:
            if day_entries:
                day_entries.sort(key=lambda x: x['timestamp'])
                start_times.append(datetime.fromtimestamp(day_entries[0]['timestamp'] / 1000.0))
                end_times.append(datetime.fromtimestamp(day_entries[-1]['timestamp'] / 1000.0))

        avg_start_time = utils.compute_average_time(start_times)
        avg_end_time = utils.compute_average_time(end_times)

        return avg_start_time, avg_end_time

    @abstractmethod
    def fuel_consumed(self, data_entries):
        """
        Method to calculate fuel consumed by the machine, using the first and last fuel levels of each day.
        """
        pass

    def __calculate_daily_seconds(self, daily_entries):
        """
        Calculates the total seconds worked for a single day from the first and last entries.
        Assumes `daily_entries` contains the entire entry (not just timestamps).
        """
        if len(daily_entries) < 2:
            return 0

        daily_entries.sort(key=lambda x: x['timestamp'])

        first_timestamp = datetime.fromtimestamp(daily_entries[0]['timestamp'] / 1000.0)
        last_timestamp = datetime.fromtimestamp(daily_entries[-1]['timestamp'] / 1000.0)
        daily_work_time = last_timestamp - first_timestamp

        return daily_work_time.total_seconds()

    def split_entries_by_day(self, data_entries):
        """
        Splits data entries into groups by day, retaining the entire entry.
        """
        days = {}
        for entry in data_entries:
            timestamp = datetime.fromtimestamp(entry['timestamp'] / 1000.0)
            date_key = timestamp.date()  # Extract the date as the key

            if date_key not in days:
                days[date_key] = []
            days[date_key].append(entry)

        return list(days.values())


class ElectricMachine(Machine):
    battery_size = models.FloatField()

    def fuel_consumed(self, data_entries):
        """
        Method to calculate fuel consumed by the machine, using the first and last fuel levels of each day.
        """
        if not data_entries:
            return 0

        daily_entries = super().split_entries_by_day(data_entries)

        return str(sum(self.__calculate_daily_consumption(entries) for entries in daily_entries)) + " kWh"

    def __calculate_daily_consumption(self, daily_entries):
        """
        Calculates the total fuel consumed for a single day by subtracting the first and last fuel levels.
        Assumes `daily_entries` contains the entire entry (not just timestamps).
        """
        if len(daily_entries) < 2:
            return 0

        daily_entries.sort(key=lambda x: x['timestamp'])

        first_battery_soc = daily_entries[0]['battery_SoC']
        last_battery_soc = daily_entries[-1]['battery_SoC']

        daily_fuel_consumption = first_battery_soc - last_battery_soc

        return daily_fuel_consumption * self.battery_size


class DieselMachine(Machine):
    fuel_tank_size = models.FloatField()

    def fuel_consumed(self, data_entries):
        """
        Method to calculate fuel consumed by the machine, using the first and last fuel levels of each day.
        """
        if not data_entries:
            return 0

        daily_entries = super().split_entries_by_day(data_entries)

        return str(sum(self.__calculate_daily_consumption(entries) for entries in daily_entries)) + " L"

    def __calculate_daily_consumption(self, daily_entries):
        """
        Calculates the total fuel consumed for a single day by subtracting the first and last fuel levels.
        Assumes `daily_entries` contains the entire entry (not just timestamps).
        """
        if len(daily_entries) < 2:
            return 0

        daily_entries.sort(key=lambda x: x['timestamp'])

        first_fuel_level = daily_entries[0]['fuel_level']
        last_fuel_level = daily_entries[-1]['fuel_level']

        daily_fuel_consumption = first_fuel_level - last_fuel_level

        return daily_fuel_consumption * self.fuel_tank_size
