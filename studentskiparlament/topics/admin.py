from django.contrib import admin
from .models import Profesori, Predmeti, Smer

# Register your models here.
admin.site.register(Profesori)
admin.site.register(Predmeti)
admin.site.register(Smer)

