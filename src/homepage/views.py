from django.http import JsonResponse




def homepage(request):
    return JsonResponse({"message": "Hello, world!"})