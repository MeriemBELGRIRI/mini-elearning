from django.contrib import admin
from .models import Course, Lesson

# Enregistrer les modèles pour qu'ils apparaissent dans l'admin
admin.site.register(Course)
admin.site.register(Lesson)
