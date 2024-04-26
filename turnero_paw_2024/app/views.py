from django.shortcuts import render

def pagina_no_encontrada(request, exception):
    return render(request, '404.html', status=404)

def internal_server_error(request):
    return render(request, '500.html', status=500)
