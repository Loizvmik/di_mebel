from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Team
from src.furniture.models import Image


@api_view(['GET'])
def get_team(request):
    try:
        team = Team.objects.first()  # Получаем первую (или единственную) команду

        if not team:
            return JsonResponse(
                {"message": "Информация о команде не найдена"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "image": {
                "id": team.image.id,
                "url": team.image.image.url if team.image and team.image.image else None
            } if team.image else None
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при получении информации о команде: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def create_team(request):
    try:
        with transaction.atomic():
            # Проверяем, существует ли уже команда
            if Team.objects.exists():
                return Response(
                    {"error": "Команда уже существует. Используйте метод обновления."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            name = request.data.get("name")
            description = request.data.get("description")
            image_id = request.data.get("image_id")

            if not name:
                return Response(
                    {"error": "Необходимо передать name"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Инициализируем image как None
            image = None

            # Если image_id передан, пытаемся найти изображение
            if image_id:
                try:
                    image = Image.objects.get(id=image_id)

                    # Проверка, что изображение не используется
                    if Team.objects.filter(image=image).exists():
                        return Response(
                            {"error": "Данное изображение уже используется"},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except Image.DoesNotExist:
                    return Response(
                        {"error": "Изображение с указанным ID не найдено"},
                        status=status.HTTP_404_NOT_FOUND
                    )

            team = Team.objects.create(
                name=name,
                description=description,
                image=image
            )

            return Response(
                {
                    "message": "Информация о команде успешно добавлена",
                    "team_id": team.id
                },
                status=status.HTTP_201_CREATED
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
def update_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)

        updated_fields = []

        if 'name' in request.data and request.data['name'] is not None:
            team.name = request.data['name']
            updated_fields.append('name')

        if 'description' in request.data and request.data['description'] is not None:
            team.description = request.data['description']
            updated_fields.append('description')

        if updated_fields:
            team.save(update_fields=updated_fields)

        data = {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "image_id": team.image.id if team.image else None
        }

        return JsonResponse(
            {
                "message": "Информация о команде обновлена",
                "team": data
            },
            status=status.HTTP_200_OK
        )

    except Team.DoesNotExist:
        return JsonResponse(
            {"error": "Команда не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при обновлении информации о команде: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
def update_team_image(request, team_id):
    try:
        team = Team.objects.get(id=team_id)

        image_id = request.data.get('image_id')

        if image_id is None:
            # Удаляем связь с изображением
            team.image = None
            team.save(update_fields=['image'])

            return JsonResponse({
                "message": "Изображение команды успешно удалено",
                "team_id": team_id
            }, status=status.HTTP_200_OK)

        try:
            image = Image.objects.get(id=image_id)

            # Проверка, что изображение не используется другой командой
            existing = Team.objects.filter(image=image).exclude(id=team_id)
            if existing.exists():
                return Response(
                    {"error": "Данное изображение уже используется"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            team.image = image
            team.save(update_fields=['image'])

            return JsonResponse({
                "message": "Изображение команды успешно обновлено",
                "team": {
                    "id": team.id,
                    "name": team.name,
                    "image": {
                        "id": image.id,
                        "url": image.image.url if image.image else None
                    }
                }
            }, status=status.HTTP_200_OK)

        except Image.DoesNotExist:
            return Response(
                {"error": "Изображение с указанным ID не найдено"},
                status=status.HTTP_404_NOT_FOUND
            )

    except Team.DoesNotExist:
        return JsonResponse(
            {"error": "Команда не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при обновлении изображения команды: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_team_by_id(request, team_id):
    try:
        team = Team.objects.get(id=team_id)

        data = {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "image": {
                "id": team.image.id,
                "url": team.image.image.url if team.image and team.image.image else None
            } if team.image else None
        }

        return JsonResponse(data)

    except Team.DoesNotExist:
        return JsonResponse(
            {"error": "Команда с указанным ID не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при получении информации о команде: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
def delete_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        name = team.name
        team.delete()

        return JsonResponse(
            {
                "message": "Информация о команде успешно удалена",
                "deleted_team": {"id": team_id, "name": name}
            },
            status=status.HTTP_200_OK
        )
    except Team.DoesNotExist:
        return JsonResponse(
            {"error": "Команда не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при удалении информации о команде: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )