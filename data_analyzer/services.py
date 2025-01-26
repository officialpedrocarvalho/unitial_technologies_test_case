from data_analyzer.factories import MachineFactory
from data_analyzer.repositories import MachineRepository


class MachineService:
    @staticmethod
    def register_machines(machines_data):
        machines = [MachineFactory.create_machine(machine_data) for machine_data in machines_data]
        MachineRepository.persist_all(machines)

    @staticmethod
    def analyze_data(entries_data):
        machines = MachineRepository.find_all()
        entries_by_machine = {machine.machine_id: [] for machine in machines}

        for entry in entries_data:
            entries_by_machine[entry['machine_id']].append(entry)

        for machine in machines:
            yield {
                'machine_id': machine.machine_id,
                'average_start': machine.average_start_end_time(entries_by_machine[machine.machine_id])[0],
                'average_end': machine.average_start_end_time(entries_by_machine[machine.machine_id])[1],
                'hours_worked': machine.hours_worked(entries_by_machine[machine.machine_id]),
                'fuel_consumed': machine.consumption(entries_by_machine[machine.machine_id])
            }
