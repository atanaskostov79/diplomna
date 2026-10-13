from .models import Category


def navigation(request):
    return {
        'categories': Category.objects.all(),
    }
