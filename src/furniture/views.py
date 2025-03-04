from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Furniture, Image
from django.http import JsonResponse
from .models import Image

@api_view(['POST'])
def create_furniture(request):
    try:
        with transaction.atomic():
            # Получаем данные из запроса
            name = request.data.get("name")
            price = request.data.get("price")
            characteristic = request.data.get("characteristic")
            category = request.data.get("category")
            # Проверка обязательных полей
            if not name or not price or not category:
                return Response(
                    {"error": "Необходимо передать name, price и category"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Создаем запись в таблице Furniture
            furniture = Furniture.objects.create(
                name=name,
                price=price,
                characteristic=characteristic,
                category=category
            )
            # Возвращаем JSON-ответ об успешном создании
            return Response(
                {"message": "Мебель успешно добавлена", "furniture_id": furniture.id},
                status=status.HTTP_201_CREATED
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def upload_image(request):
    # Проверяем, что файл передан
    if 'image' not in request.FILES:
        return Response({'error': 'Файл изображения не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
    
    image_file = request.FILES['image']
    furniture_id = request.data.get('furniture_id')
    if not furniture_id:
        return Response({'error': 'Необходимо выбрать фотографию'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # Создаем запись в модели Image. Поле image настроено с upload_to='images/'
        image_instance = Image.objects.create(image=image_file,furniture_id=furniture_id)
        return Response({
            'message': 'Изображение успешно загружено',
            'image_id': image_instance.id,
            'furniture_id': furniture_id
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)