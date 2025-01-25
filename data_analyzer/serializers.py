from rest_framework import serializers

from .models.data import DataEntry
from .models.machine import ElectricMachine, DieselMachine

class ElectricMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricMachine
        fields = ['machine_id', 'manufacturer', 'type', 'battery_size']

class DieselMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DieselMachine
        fields = ['machine_id', 'manufacturer', 'type', 'fuel_tank_size']

class DataEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataEntry
        fields = '__all__'
