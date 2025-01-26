from collections import defaultdict

from data_analyzer.models.machine import ElectricMachine, DieselMachine


class MachineRepository:
    @staticmethod
    def find_all():
        return list(ElectricMachine.objects.all()) + list(DieselMachine.objects.all())

    @staticmethod
    def persist_all(machines):
        machine_groups = defaultdict(list)

        for machine in machines:
            if isinstance(machine, ElectricMachine):
                machine_groups[ElectricMachine].append(machine)
            elif isinstance(machine, DieselMachine):
                machine_groups[DieselMachine].append(machine)

        if machine_groups[ElectricMachine]:
            ElectricMachine.objects.bulk_create(machine_groups[ElectricMachine])
        if machine_groups[DieselMachine]:
            DieselMachine.objects.bulk_create(machine_groups[DieselMachine])
