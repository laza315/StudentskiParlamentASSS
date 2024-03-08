from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from topics.models import Profesori, Predmeti, Smer
from django.core.exceptions import ValidationError
from django_enum import EnumField
from django.core.validators import MaxValueValidator, MinValueValidator


class Anketa(models.Model):
    INFORMATIKA = "Informatika"
    DRUMSKI_SAOBRACAJ = "Drumski Saobracaj"
    PRIVREDNO_INZINJERSTVO = "Privredno Inzinjerstvo"

    SMER_CHOICES = [
        (INFORMATIKA, "Informatika"),
        (DRUMSKI_SAOBRACAJ, "Drumski Saobracaj"),
        (PRIVREDNO_INZINJERSTVO, "Privredno Inzinjerstvo"),
    ]
    class AnketaType(models.IntegerChoices):
        PROFESORI = 1, 'Profesori'
        PREDMETI = 2, 'Predmeti'

    id = models.AutoField(primary_key=True)
    host_id=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    naziv = models.CharField(max_length=255, default='', blank=True)
    smer = models.CharField(
                    max_length=255,
                    choices=SMER_CHOICES, 
                    default=INFORMATIKA, 
                    blank=False, 
                    null=False
                )
    tip_ankete = EnumField(enum=AnketaType, default=AnketaType.PROFESORI, blank=False, null=False)
    godina = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(3), MinValueValidator(1)]) 
    broj_kodova = models.IntegerField(default=10, null=False, validators=[MaxValueValidator(150), MinValueValidator(1)])
    broj_pitanja = models.IntegerField(default=1, null=False, validators=[MaxValueValidator(5), MinValueValidator(1)])
    vreme_do = models.DateTimeField(default=timezone.now)
    opis_ankete = models.TextField(null=True, blank=True)
    publish_date = models.DateTimeField(default=timezone.now)
    aktivnost = models.BooleanField(default=False)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return f'Anketa:{self.id}. Korisnik sa {self.host_id} id, je napravio anketu o {self.get_tip_ankete_display()}ma pod Nazivom: {self.naziv} za {self.godina} godinu i za smer: {self.smer}. Anketu je namenjeno da oceni najvise {self.broj_kodova} studenta. Anketa se sastoji od {self.broj_pitanja} pitanja i bice aktivna do {self.vreme_do}. Opis: {self.opis_ankete}. Kreirana: u {self.publish_date}. Aktivna = {self.aktivnost}.'
    
    
class BackUpKod(models.Model):

    id = models.AutoField(primary_key=True)
    anketa = models.ForeignKey(Anketa, on_delete=models.CASCADE, null=False)
    code_value = models.CharField(max_length=10, unique=True, validators=[MinLengthValidator(limit_value=4)])
    is_used = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    code_duration = models.DurationField(default=timedelta(days=15),null=True, blank=True)

class VezaProfesori(models.Model):
    
    anketa = models.ForeignKey(Anketa, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesori, on_delete=models.CASCADE)

class VezaPredmeti(models.Model):
    
    anketa=models.ForeignKey(Anketa, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)

class VezaSmer(models.Model):
    
    anketa=models.ForeignKey(Anketa, on_delete=models.CASCADE)
    smer = models.ForeignKey(Smer, on_delete=models.CASCADE)


class Pitanja(models.Model):
    
    anketa = models.ForeignKey(Anketa, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    redni_broj = models.PositiveIntegerField(default=1) 

    # def save(self, *args, **kwargs):
    #     max_redni_broj = Pitanja.objects.filter(anketa=self.anketa).count() + 1
    #     if max_redni_broj > 5:
    #         raise ValidationError("Maximum number of questions exceeded.")
    #     self.redni_broj = max_redni_broj
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Pitanje: {self.question_text} sa ID:  {self.id} i redni broj {self.redni_broj} za anketu {self.anketa.id}"
    
    def save_choices_for_question(self, anketa, choices):
        question = Pitanja.objects.get(anketa=anketa)
        existing_choices = Izbori.objects.filter(question=question)
        if not existing_choices.exists():
            for choice in choices:
                Izbori.objects.create(question=question, choice_text=choice)
        else:
            return


class Izbori(models.Model):
    
    
    question =  models.ForeignKey(Pitanja, on_delete=models.CASCADE, null=False)
    choice_text = models.CharField(max_length=255)


    def __str__(self):
        return self.choice_text



class Vote(models.Model):

    VOTE_CHOICES = (
        (1, 'Nisam zadovoljan'),
        (2, 'Onako'),
        (3, 'Zadovoljan'),
        (4, 'Odlično'),
    )

    choice = models.ForeignKey(Izbori, on_delete=models.CASCADE)
    kod_value = models.ForeignKey(BackUpKod, on_delete=models.SET_NULL, null=True) 
    votes = models.IntegerField(choices=VOTE_CHOICES, default='3')
    




















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
         
