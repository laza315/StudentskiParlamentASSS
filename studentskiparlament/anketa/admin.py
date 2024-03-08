from django.contrib import admin
from .models import Anketa, BackUpKod, Pitanja, Izbori, Vote

# Register your models here.
admin.site.register(Anketa)
admin.site.register(BackUpKod)

class ChoiceInLine(admin.TabularInline):
    model = (Izbori)
    extra = 15

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
                  (None, {'fields':['question_text']}),
                  ('Anketa', {'fields': ['anketa']}),
                ]
    inlines = [ChoiceInLine]

admin.site.register(Pitanja, QuestionAdmin)
admin.site.register(Vote)
