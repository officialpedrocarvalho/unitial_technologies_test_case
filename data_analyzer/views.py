import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from data_analyzer.services import MachineService


# Endpoint 1: Register new machines
@api_view(['POST'])
def register_machines(request):
    try:
        machines_data = json.loads(request.body)
        MachineService.register_machines(machines_data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Machines registered successfully!"}, status=status.HTTP_201_CREATED)


# Endpoint 2: Get Machine analysis
@api_view(['GET'])
def machine_analysis(request):
    try:
        entries_data = json.loads(request.body)
        analysis_results = MachineService.analyze_data(entries_data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(analysis_results)


# Endpoint 3: Get the day with the highest consumption
@api_view(['GET'])
def highest_consumption_day(request):
    try:
        entries_data = json.loads(request.body)
        # result = MachineService.compute_highest_consumption_day(entries_data) TODO: Implement logic
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response()
