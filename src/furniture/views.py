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

@api_view(['GET'])
def get_furniture(request):
    # Получение списка всей мебели
    furnitures = Furniture.objects.all()
    data = [
        {
            "id": furniture.id,
            "name": furniture.name,
            "price": furniture.price,
            "characteristic": furniture.characteristic,
            "category": furniture.category,
            "images": [
                {
                    "id": img.id,
                    "name": img.name,
                    "image": img.image.url if img.image else None,
                    "category": img.category
                }
                for img in furniture.images.all()
            ]
        }
        for furniture in furnitures
    ]
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def get_furniture_by_id(request, forniture_id):
    try:
        furniture = Furniture.objects.get(id=forniture_id)
        data = {
            "id": furniture.id,
            "name": furniture.name,
            "price": furniture.price,
            "characteristic": furniture.characteristic,
            "category": furniture.category,
            "images": [
                {
                    "id": img.id,
                    "name": img.name,
                    "image": img.image.url if img.image else None,
                    "category": img.category
                }
                for img in furniture.images.all()
            ]
        }
        return JsonResponse(data, safe=False)
    except Furniture.DoesNotExist:
        return JsonResponse({"error": "Мебель не найдена"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_furniture_data(request, furniture_id):
    try:
        furniture = Furniture.objects.get(id=furniture_id)

        # Получаем данные из запроса только если они предоставлены
        updated_fields = []

        # Проверяем каждое поле и обновляем только если оно есть в запросе
        if 'name' in request.data and request.data['name'] is not None:
            furniture.name = request.data['name']
            updated_fields.append('name')

        if 'price' in request.data and request.data['price'] is not None:
            try:
                furniture.price = int(request.data['price'])
                updated_fields.append('price')
            except (ValueError, TypeError):
                return JsonResponse(
                    {"error": "Поле price должно быть числом"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if 'characteristic' in request.data and request.data['characteristic'] is not None:
            furniture.characteristic = request.data['characteristic']
            updated_fields.append('characteristic')

        if 'category' in request.data and request.data['category'] is not None:
            furniture.category = request.data['category']
            updated_fields.append('category')

        # Сохраняем только если были обновления
        if updated_fields:
            furniture.save(update_fields=updated_fields)

        # Формируем ответ
        data = {
            "id": furniture.id,
            "name": furniture.name,
            "price": furniture.price,
            "category": furniture.category
        }

        return JsonResponse(
            {
                "message": "Мебель успешно обновлена",
                "furniture": data
            },
            status=status.HTTP_200_OK
        )

    except Furniture.DoesNotExist:
        return JsonResponse({"error": "Мебель не найдена"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при обновлении мебели: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
def delete_furniture(request, furniture_id):
    try:
        furniture = Furniture.objects.get(id=furniture_id)
        data = {
            "id": furniture.id,
            "name": furniture.name,
        }
        furniture.delete()
        return JsonResponse(
            {"message": "Мебель успешно удалена", "deleted_item": data},
            status=status.HTTP_200_OK)
    except Furniture.DoesNotExist:
        return JsonResponse({"error": "Мебель не найдена"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при удалении мебели: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
def add_furniture_images(request, furniture_id):
    try:
        furniture = Furniture.objects.get(id=furniture_id)

        # Получаем список ID изображений из запроса
        image_ids = request.data.get("images", [])
        if not isinstance(image_ids, list):
            return JsonResponse(
                {"error": "Поле 'images' должно быть списком ID изображений"},
                status=status.HTTP_400_BAD_REQUEST
            )

        added_ids = []
        not_found_ids = []

        # Обрабатываем каждое изображение
        if image_ids:
            images = Image.objects.filter(id__in=image_ids)

            # Находим ID, которых нет в базе
            found_ids = [img.id for img in images]
            not_found_ids = [img_id for img_id in image_ids if img_id not in found_ids]

            # Привязываем изображения к мебели
            for image in images:
                image.furniture_id = furniture  # Используем объект furniture, а не его ID
                image.save()
                added_ids.append(image.id)

        response_data = {
            "id": furniture.id,
            "name": furniture.name,
            "added_images": added_ids
        }

        # Добавляем информацию о ненайденных изображениях, если они есть
        if not_found_ids:
            response_data["not_found_images"] = not_found_ids

        return JsonResponse(
            {
                "message": "Изображения успешно добавлены к мебели",
                "furniture": response_data
            },
            status=status.HTTP_200_OK
        )
    except Furniture.DoesNotExist:
        return JsonResponse({"error": "Мебель не найдена"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при добавлении изображений: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
def update_furniture_images(request, furniture_id):
    try:
        furniture = Furniture.objects.get(id=furniture_id)
        image_ids = request.data.get("images", [])

        if not isinstance(image_ids, list):
            return JsonResponse(
                {"error": "Поле 'images' должно быть списком ID изображений"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Отвязываем все текущие изображения от мебели
        Image.objects.filter(furniture_id=furniture).update(furniture_id=None)

        attached_image_ids = []
        not_found_ids = []

        if image_ids:
            # Получаем все изображения, которые существуют
            images = Image.objects.filter(id__in=image_ids)

            # Находим ID, которые не существуют в базе данных
            found_ids = [img.id for img in images]
            not_found_ids = [img_id for img_id in image_ids if img_id not in found_ids]

            # Привязываем найденные изображения к мебели
            for image in images:
                image.furniture_id = furniture
                image.save()
                attached_image_ids.append(image.id)

        response_data = {
            "id": furniture.id,
            "name": furniture.name,
            "attached_image_ids": attached_image_ids
        }

        # Добавляем информацию о ненайденных изображениях, если они есть
        if not_found_ids:
            response_data["not_found_image_ids"] = not_found_ids

        return JsonResponse(
            {
                "message": "Изображения мебели обновлены",
                "furniture": response_data
            },
            status=status.HTTP_200_OK
        )
    except Furniture.DoesNotExist:
        return JsonResponse({"error": "Мебель не найдена"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при обновлении изображений: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
