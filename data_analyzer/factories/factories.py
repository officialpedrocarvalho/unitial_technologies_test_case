from data_analyzer.models.machine import ElectricMachine, DieselMachine


class MachineFactory:
    @staticmethod
    def create_machine(machine_data):
        """
        Factory method to create a machine based on its fuel type.
        """
        if machine_data['fuel_type'] == 'electric':
            return ElectricMachine(
                machine_id=machine_data['id'],
                manufacturer=machine_data['manufacturer'],
                type=machine_data['type'],
                battery_size=machine_data['battery_size']
            )
        elif machine_data['fuel_type'] == 'diesel':
            return DieselMachine(
                machine_id=machine_data['id'],
                manufacturer=machine_data['manufacturer'],
                type=machine_data['type'],
                fuel_tank_size=machine_data['fuel_tank_size']
            )
        else:
            raise ValueError(f"Unsupported fuel type: {machine_data['fuel_type']}")
