class DataEntry:
    def __init__(self, timestamp, machine_id, fuel_level=None, battery_SoC=None):
        self.timestamp = timestamp
        self.machine_id = machine_id
        self.fuel_level = fuel_level  # For diesel machines
        self.battery_SoC = battery_SoC  # For electric machines

    def __repr__(self):
        return f"DataEntry(machine_id={self.machine_id}, timestamp={self.timestamp}, fuel_level={self.fuel_level}, battery_SoC={self.battery_SoC})"
