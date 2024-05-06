import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import AditionalInformation

def aditional_information_api(request):
    information = AditionalInformation.objects.all().values('title', 'description', 'icon', 'link')
    serialized_information = []
    for info in information:
        icon_base64 = info['icon']
        info['icon'] = icon_base64
        serialized_information.append(info)
    return JsonResponse(serialized_information, safe=False)

def delete_aditional_information(request, pk):
    if request.method == 'POST':
        aditional_information = get_object_or_404(AditionalInformation, pk=pk)
        aditional_information.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
def update_aditional_information(request, pk):
    if request.method == 'POST':
        aditional_information = get_object_or_404(AditionalInformation, pk=pk)
        data = json.loads(request.body)
        aditional_information.title = data['title']
        aditional_information.description = data['description']
        aditional_information.link = data['link']
        aditional_information.icon = data['icon_base64']
        aditional_information.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)