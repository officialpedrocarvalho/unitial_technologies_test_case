from data_analyzer.models.machine import ElectricMachine, DieselMachine


class MachineRepository:
    @staticmethod
    def find_all():
         return list(ElectricMachine.objects.all()) + list(DieselMachine.objects.all())