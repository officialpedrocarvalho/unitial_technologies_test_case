from data_analyzer.factories.factories import MachineFactory
from data_analyzer.models.machine import ElectricMachine, DieselMachine
from data_analyzer.repositories.repositories import MachineRepository


class MachineService:
    @staticmethod
    def register_machines(machines_data):
        electric_machines = []
        diesel_machines = []

        for machine_data in machines_data:
            machine = MachineFactory.create_machine(machine_data)
            if isinstance(machine, ElectricMachine):
                electric_machines.append(machine)
            elif isinstance(machine, DieselMachine):
                diesel_machines.append(machine)

        if electric_machines:
            ElectricMachine.objects.bulk_create(electric_machines)
        if diesel_machines:
            DieselMachine.objects.bulk_create(diesel_machines)

        return

    @staticmethod
    def analyze_data(entries_data):
        machines = MachineRepository.find_all()

        analysis_results = []
        for machine in machines:
            machine_data_entries = [entry for entry in entries_data if entry['machine_id'] == machine.machine_id]

            average_start, average_end = machine.average_start_end_time(machine_data_entries)
            hours_worked = machine.hours_worked(machine_data_entries)
            fuel_consumed = machine.fuel_consumed(machine_data_entries)

            analysis_results.append({
                'machine_id': machine.machine_id,
                'average_start': average_start,
                'average_end': average_end,
                'hours_worked': hours_worked,
                'fuel_consumed': fuel_consumed
            })

        return analysis_results
