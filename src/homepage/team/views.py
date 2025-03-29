from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from src.homepage.models import Team
from src.furniture.models import Image


@api_view(['POST'])
def create_team(request):
    try:
        with transaction.atomic():
            name = request.data.get("name")
            description = request.data.get("description")
            image_id = request.data.get("image_id")

            # Проверяем только name как обязательное поле
            if not name:
                return Response(
                    {"error": "Необходимо передать name"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Создаем базовую команду без изображения
            team = Team.objects.create(
                name=name,
                description=description
            )

            # Если передан image_id, пытаемся привязать изображение
            if image_id:
                try:
                    image = Image.objects.get(id=image_id)

                    # Проверяем, не привязано ли изображение к другой команде
                    if hasattr(image, 'team'):
                        # Откатываем транзакцию, так как команда уже создана
                        return Response(
                            {"error": "Это изображение уже привязано к другой команде"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # Привязываем изображение к команде
                    team.image = image
                    team.save(update_fields=['image'])
                except Image.DoesNotExist:
                    # Команду все равно создаем, но возвращаем предупреждение
                    return Response(
                        {
                            "message": "Команда успешно создана, но изображение не найдено",
                            "team_id": team.id,
                            "warning": "Изображение с указанным ID не найдено"
                        },
                        status=status.HTTP_201_CREATED
                    )

            return Response(
                {"message": "Команда успешно создана", "team_id": team.id},
                status=status.HTTP_201_CREATED
            )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_teams(request):
    try:
        teams = Team.objects.all()

        if not teams.exists():
            return JsonResponse(
                {"message": "Команды не найдены в базе данных"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = [
            {
                "id": team.id,
                "name": team.name,
                "description": team.description,
                "image": {
                    "id": team.image.id,
                    "url": team.image.image.url if team.image and team.image.image and hasattr(team.image.image,
                                                                                               'url') else None,
                    "category": team.image.category if team.image else None
                } if team.image else None
            }
            for team in teams
        ]

        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при получении списка команд: {str(e)}"},
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
                "url": team.image.image.url if team.image and team.image.image and hasattr(team.image.image,
                                                                                           'url') else None,
                "category": team.image.category if team.image else None
            } if team.image else None
        }

        return JsonResponse(data, safe=False)
    except Team.DoesNotExist:
        return JsonResponse(
            {"error": "Команда не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка: {str(e)}"},
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
            team.save()

        data = {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "image_id": team.image.id if team.image is not None else None
        }

        return JsonResponse(
            {"message": "Команда успешно обновлена", "team": data},
            status=status.HTTP_200_OK
        )
    except Team.DoesNotExist:
        return JsonResponse(
            {"error": "Команда не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при обновлении команды: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
def add_image_to_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        image_id = request.data.get('image_id')

        if not image_id:
            return JsonResponse(
                {"error": "Необходимо указать image_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return JsonResponse(
                {"error": "Изображение с указанным ID не найдено"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, не привязано ли изображение к другой команде
        if hasattr(image, 'team') and image.team.id != team.id:
            return JsonResponse(
                {"error": "Это изображение уже привязано к другой команде"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Обновляем связь (изображение может заменить существующее или быть добавлено впервые)
        team.image = image
        team.save(update_fields=['image'])

        return JsonResponse({
            "message": "Изображение успешно добавлено к команде",
            "team": {
                "id": team.id,
                "name": team.name,
                "image": {
                    "id": image.id,
                    "url": image.image.url if image.image and hasattr(image.image, 'url') else None,
                    "category": image.category
                }
            }
        }, status=status.HTTP_200_OK)

    except Team.DoesNotExist:
        return JsonResponse(
            {"error": "Команда не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при добавлении изображения к команде: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
def delete_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        data = {
            "id": team.id,
            "name": team.name
        }
        team.delete()
        return JsonResponse(
            {"message": "Команда успешно удалена", "deleted_item": data},
            status=status.HTTP_200_OK
        )
    except Team.DoesNotExist:
        return JsonResponse(
            {"error": "Команда не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Произошла ошибка при удалении команды: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )