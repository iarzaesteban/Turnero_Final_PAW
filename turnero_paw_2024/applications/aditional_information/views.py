import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import AditionalInformation

def aditional_information_api(request):
    if request.method == "GET":
        information = AditionalInformation.get_all_information()
        return JsonResponse(information, safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def delete_aditional_information(request, pk):
    if request.method == "POST":
        aditional_information = get_object_or_404(AditionalInformation, pk=pk)
        aditional_information.delete_information()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Método no permitido"}, status=405)
    
def update_aditional_information(request, pk):
    if request.method == "POST":
        print(f"VAMOS A ACTUALIZAR UN info {pk}", flush=True)
        aditional_information = get_object_or_404(AditionalInformation, pk=pk)
        data = json.loads(request.body)
        aditional_information.update_information(data)
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Método no permitido"}, status=405)