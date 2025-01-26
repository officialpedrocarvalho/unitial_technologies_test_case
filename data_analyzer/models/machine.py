from abc import abstractmethod
from datetime import datetime

from django.db import models

from data_analyzer import utils


class Machine(models.Model):
    machine_id = models.CharField(max_length=255, unique=True)
    manufacturer = models.CharField(max_length=255)
    type = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def hours_worked(self, data_entries):
        """
        Calculate the total number of hours the machine has worked.
        """
        daily_entries = utils.split_entries_by_day(data_entries)
        return round(sum(utils.calculate_daily_seconds(entries) for entries in daily_entries) / 3600)

    def average_start_end_time(self, data_entries):
        """
        Computes the average start and end of a machine's work grouping by day.
        """
        days_entries = utils.split_entries_by_day(data_entries)

        start_times = []
        end_times = []
        for day_entries in days_entries:
            day_entries.sort(key=lambda x: x['timestamp'])
            start_times.append(datetime.fromtimestamp(day_entries[0]['timestamp'] / 1000.0))
            end_times.append(datetime.fromtimestamp(day_entries[-1]['timestamp'] / 1000.0))

        return utils.compute_average_time(start_times), utils.compute_average_time(end_times)

    @abstractmethod
    def consumption(self, data_entries):
        """
        Calculates the machine's consumption.
        """
        pass


class ElectricMachine(Machine):
    battery_size = models.FloatField()

    def consumption(self, data_entries):
        """
        Calculates the machine's consumption, using the first and last battery levels of each day.
        """
        daily_entries = utils.split_entries_by_day(data_entries)
        return round(sum(self.__calculate_daily_consumption(entries) for entries in daily_entries), 2)

    def __calculate_daily_consumption(self, daily_entries):
        if len(daily_entries) < 2:
            return 0

        daily_entries.sort(key=lambda x: x['timestamp'])
        first_battery_soc = daily_entries[0]['battery_SoC']
        last_battery_soc = daily_entries[-1]['battery_SoC']

        return (first_battery_soc - last_battery_soc) * self.battery_size


class DieselMachine(Machine):
    fuel_tank_size = models.FloatField()

    def consumption(self, data_entries):
        """
        Calculates the machine's consumption, using the first and last fuel levels of each day.
        """
        daily_entries = utils.split_entries_by_day(data_entries)
        return round(sum(self.__calculate_daily_consumption(entries) for entries in daily_entries), 2)

    def __calculate_daily_consumption(self, daily_entries):
        if len(daily_entries) < 2:
            return 0

        daily_entries.sort(key=lambda x: x['timestamp'])
        first_fuel_level = daily_entries[0]['fuel_level']
        last_fuel_level = daily_entries[-1]['fuel_level']

        return (first_fuel_level - last_fuel_level) * self.fuel_tank_size
