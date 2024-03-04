from django.db import models

class Profesori(models.Model):

    id = models.AutoField(primary_key=True)
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=100)
    godina = models.PositiveIntegerField()
    smer = models.ManyToManyField('Smer', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Kreiran je profesor {self.ime} {self.prezime} koji predaje na {[s.naziv_smera for s in self.smer.all()]} smeru, na {self.godina} godini, u {self.date_created}.'

class Predmeti(models.Model):

    id = models.AutoField(primary_key=True)
    naziv_predmeta = models.CharField(max_length=255)
    godina = models.PositiveIntegerField()
    smer = models.ManyToManyField('Smer', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Kreiran je predmet {self.naziv_predmeta} za smer: {[s.naziv_smera for s in self.smer.all()]} na {self.godina} godini, u {self.date_created}.'

class Smer(models.Model):

    id = models.AutoField(primary_key=True)
    naziv_smera = models.CharField(max_length=255)
    smerovi_profesora = models.ManyToManyField(Profesori, blank=True, related_name='smerovi_profesora')
    smerovi_predmeta = models.ManyToManyField(Predmeti, blank=True, related_name='smerovi_predmeta')

    def __str__(self):
        return f'Smer {self.naziv_smera} je kreiran.'
