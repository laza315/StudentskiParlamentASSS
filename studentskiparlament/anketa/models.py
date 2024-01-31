from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

class Anketa(models.Model):

    id = models.AutoField(primary_key=True)
    host_id=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    naziv = models.CharField(max_length=255, default='', blank=True)
    # smer_id = models.ForeignKey(StudijskiProgram, nullable=False)
    # profesori_id = models.ForeignKey(Profesori, nullable=False)
    # predmeti_id = models.IntegerField
    # godina = models.IntegerField
    broj_kodova = models.IntegerField(default=10)
    opis_ankete = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return f'Korisnik sa {self.host_id} id, je napravio anketu u {self.publish_date} pod Nazivom: {self.naziv} za {self.broj_kodova}.Opis: {self.opis_ankete}.'

class BackUpKod(models.Model):

    id = models.AutoField(primary_key=True)
    anketa = models.ForeignKey(Anketa, on_delete=models.CASCADE, null=False)
    code_value = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(limit_value=4)])
    is_used = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    code_duration = models.DurationField(default=timedelta(days=15),null=True, blank=True)























    # def Predmeti():
    # if host izabere anketu o predmetima:
    #     def __str__(self):
    #         return f'Korisnik sa id {host_id} je napravio anketu o {predmeti_id} na {godina} godini, za {smer_id} studijski_program i {broj_kodova} studenata.<br>
    #             Opis: {opis_ankete}.<br>
    #             Objavljeno: {publish_date}.'
    # # elif host izabere anketu o profesorima:
    #     def __str__(self):
    #         return f'Korisnik sa id {host_id} je napravio anketu o {profesori_id} profesorima, na {godina} godini, za {smer_id} studijski_program i {broj_kodova} studenata.<br>
    #             Opis: {opis_ankete}.<br>
    #             Objavljeno: {publish_date}.'
    # else
    # print('Nesto nije poslo kako treba') 
         
