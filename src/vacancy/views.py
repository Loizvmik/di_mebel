import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Vacancy, VacancyPerson
from django.shortcuts import render, redirect
from .forms import VacancyPersonForm

@csrf_exempt
@require_http_methods(["POST"])
def create_vacancy_view(request):
    """
    Создаёт vacancy.
    Ожидает JSON с полями: work, name, description, phone.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
        work = data.get("work")

        if not work:
            return JsonResponse({"error": "Не переданы все необходимые поля."}, status=400)

        # Создаем вакансию
        vacancy = Vacancy.objects.create(work=work)

        return JsonResponse({
            "vacancy": {
                "id": vacancy.id,
                "work": vacancy.work,
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_vacancy_view(request, vacancy_id):
    """
    Удаляет вакансию по её id.
    Связанная запись VacancyPerson будет удалена автоматически.
    """
    try:
        vacancy = Vacancy.objects.get(id=vacancy_id)
        vacancy.delete()
        return JsonResponse({"message": "Вакансия успешно удалена."}, status=200)
    except Vacancy.DoesNotExist:
        return JsonResponse({"error": "Вакансия не найдена."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def create_vacancy_person_view(request):
    """
    Отображает форму для создания VacancyPerson и обрабатывает отправку данных.
    """
    if request.method == 'POST':
        form = VacancyPersonForm(request.POST)
        if form.is_valid():
            form.save()
            # Редирект на нужную страницу после успешного создания записи
            return redirect('success_url')  # замените 'success_url' на нужный URL или имя URL из вашего проекта
    else:
        form = VacancyPersonForm()

    return render(request, '', {'form': form})


@require_http_methods(["DELETE"])
def delete_vacancy_person_by_phone_view(request, phone):
    """
    Удаляет объект VacancyPerson по номеру телефона.

    Параметры:
      phone: номер телефона, по которому идентифицируется VacancyPerson.
    """
    try:
        vacancy_person = VacancyPerson.objects.get(phone=phone)
        vacancy_person.delete()
        return JsonResponse({"message": "VacancyPerson успешно удалён."}, status=200)
    except VacancyPerson.DoesNotExist:
        return JsonResponse({"error": "VacancyPerson с данным номером телефона не найден."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)