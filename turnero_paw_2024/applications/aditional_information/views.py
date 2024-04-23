import base64

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
