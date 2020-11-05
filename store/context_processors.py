from .models import Category, GENDER_CHOICES


def static_categories(request):
    categories = Category.objects.all()
    genders = [gender[0] for gender in GENDER_CHOICES]
    return {'static_categories': categories, 'genders': genders}

