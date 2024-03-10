from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import AnketaForm, PitanjaForm, VotesForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.mail import send_mail
from .code_generator import CodeGenerator
from . models import BackUpKod, Anketa, Pitanja, Izbori, Vote
from topics.models import Smer, Profesori, Predmeti
from django.db.models import F
from django.utils.html import strip_tags
from django.core.paginator import Paginator, Page
from time import timezone, time
from datetime import datetime, date
import time
from django.utils import timezone
from django.utils.timezone import make_naive


#Create your views here.
def landing_page(request):
    return render(request, 'anketa/landing_page.html')


@method_decorator(login_required(login_url='hostlogin'), name='dispatch')
class PasswordsChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'anketa/hostprofile.html'
    success_url = reverse_lazy('hostlogin')

@login_required(login_url='hostlogin')
def user_surveys(request, pk):
    user = User.objects.get(pk=pk)
    anketa = Anketa.objects.filter(host_id=user).all()
    # room_message = user.message_set.all()
    # topics = Topic.objects.all()
    paginator = Paginator(anketa, 10)  
    page_number = request.GET.get('page')
    anketa = paginator.get_page(page_number)
    context = {
        'user': user, 
        'anketa': anketa,
    }
    return render(request, 'anketa/mojeankete.html', context)

@login_required(login_url='hostlogin')
def survay_details(request, pk):
    anketa_details = Anketa.objects.get(id=pk)
    anketna_pitanja = Pitanja.objects.filter(anketa_id=anketa_details).all()
    izbori = Izbori.objects.filter(question__in=anketna_pitanja)
    context = {
        'anketa_details': anketa_details,
        'anketna_pitanja': anketna_pitanja,
        'izbori': izbori
    }
    return render(request, 'anketa/details.html', context)


def hosthomepage(request):
    obj=User.objects.all()
    hosts = {
        "obj": obj
    }
    return render(request, "anketa/hosthomepage.html", hosts)

@login_required(login_url='hostlogin')
def profile(request):
    # user = User.objects.get(pk=pk)
    # context = {'user': user}
    return render(request, 'anketa/hostprofile.html')

@login_required(login_url='hostlogin')
def host_makes_anketa(request):
    if request.user.is_authenticated: 
        if request.method == 'POST':
            form = AnketaForm(request.POST)
            if form.is_valid():
                anketa = form.save(commit=False)
                anketa.host_id = request.user
                anketa.save()
                print(f'Anketa sa id: {anketa.id},  je uspesno napravljena')

                codes = CodeGenerator.generate_codes()
                mail_bkcodes_sender(request, codes, anketa)
                messages.success(request, f'Anketa " {anketa.naziv} " o {anketa.get_tip_ankete_display()}ma,  za smer {anketa.smer} na {anketa.godina} godini, je uspesno kreirana! Vasa Anketa je trenutno aktivna i bice dostupna do {anketa.vreme_do}.')
                time.sleep(2)
                #return redirect('email')
                return redirect('pitanja', anketa_id=anketa.id)
            else:
                messages.error(request, 'error ocured')
        else:
            form = AnketaForm()

        context = {'form': form}
        return render(request, 'anketa/anketa.html', context)
    else:
        messages.warning(request, 'Molim vas da se ulogujete')
        return redirect('hostlogin')
    
@login_required(login_url='hostlogin')
def definisanje_pitanja(request, anketa_id):
    anketa = get_object_or_404(Anketa, id=anketa_id)
    br_pitanja = anketa.broj_pitanja

    if request.method == 'POST':
        pitanja_forms = [PitanjaForm(request.POST) for _ in range(br_pitanja)] # mislim da je ovde problem sa cuvanjem, overlap texta dva pitanja
        if all(form.is_valid() for form in pitanja_forms):
            for form in pitanja_forms:
                pitanje = form.save(commit=False)
                pitanje.anketa = anketa
                pitanje.save()
                time.sleep(2)
                print(f'Kreirano je pitanje: {pitanje.id}')
            

            return redirect ('pregled_ankete', anketa_id=anketa.id, pitanje_id=pitanje.id)   
            # make sure to return ('email') after you finish
    else:
        pitanja_forms = [PitanjaForm() for _ in range(br_pitanja)]

    context = {'pitanja_forms': pitanja_forms, 'anketa': anketa}
    return render(request, 'anketa/pitanja.html', context)

    
@login_required(login_url='hostlogin')
def query_za_izbor(request, anketa_id, pitanje_id): 
    pitanje_id = Pitanja.objects.filter(anketa_id=anketa_id)
    if pitanje_id.exists():
        pitanje = pitanje_id.first()
        print(pitanje.id)
    else:
        raise Http404('Pitanje ne postoji')

    try:
        anketa = get_object_or_404(Anketa, id=anketa_id)
        print(f'Lets see which anketa_id did i got : {anketa.id}')
    except Anketa.DoesNotExist:
        raise Http404("Anketa doesn't exist")
    try:
        smer_choice = anketa.smer
        print(f'Korisnik je izabrao smer: {smer_choice}')
        godina_choice = anketa.godina
        print(f'Korisnik je izabrao godinu: {godina_choice}')
        tip_ankete_choice = anketa.tip_ankete
        print(f'Korisnik je za tip_ankete izabrao: {tip_ankete_choice}')
    except:
        raise ValueError(f'Something went wrong for anketa: {anketa_id}')
    
    # TO DO - Razdvoj u posebne metode
    if tip_ankete_choice == 1:
        print('Svi Profesori')
        data_profesori = Profesori.objects.filter(
            smer__naziv_smera=smer_choice,
            godina=godina_choice).values_list('ime', 'prezime')
        choices = [' '.join(row) for row in data_profesori]
        choices_list = list(choices)
        pitanje.save_choices_for_question(anketa, choices_list)

        if request.method == 'POST':
            host_release_anketa_in_etar(request, anketa.id)
            return redirect('email')

        return render(request, 'anketa/pregled_ankete.html', {
            'data_profesori': data_profesori,
            'data_pitanje': pitanje.question_text,
            'anketa': anketa,
            'pitanje': pitanje
            })
    # TO DO - Razdvoj u posebne metode
    elif tip_ankete_choice == 2:
        print('Svi Predmeti')
        data_predmeti = Predmeti.objects.filter(
            smer__naziv_smera=smer_choice,
            godina=godina_choice).values_list('naziv_predmeta', flat=True)
        choices = list(data_predmeti)
        pitanje.save_choices_for_question(anketa, choices)
        if request.method == 'POST':
            host_release_anketa_in_etar(request, anketa.id)
            return redirect('email')

        return render(request, 'anketa/pregled_ankete.html', {
            'data_predmeti': data_predmeti,
            'data_pitanje': pitanje.question_text,
            'anketa': anketa,
            'pitanje': pitanje
            })
    else:
        return HttpResponse('Nevalidan tip ankete')
    
@login_required(login_url='hostlogin')
def host_release_anketa_in_etar(request, anketa_id):
    anketa = get_object_or_404(Anketa, id=anketa_id)
    if request.method == 'POST':
        anketa.aktivnost = True
        anketa.save()
        print(reverse('email'))

def mail_bkcodes_sender(request, number_of_codes, anketa):
    user = request.user
    email_recepient = user.email

    codes_message = ""
    for code in number_of_codes:
        codes_message += f"{code}<br>"

    message = f"<p>Поштовани,</p> <p>У следећем прилогу су кодови за Ваше студенте за Анкету под бројем {anketa.id}:</p><br>{codes_message}<br><hr><br> <p> Овај мејл је аутоматски, молимо Вас не реплицирајте на њега. Уколико имате неких питања, не устручавајте се да нас контактирате на studentska.sluzba@vts.edu.rs. </p> <p> Хвала </p>"

    send_mail (
        subject='Студентски Парламент - Академија Струковних Студија Шумадија',
        message=strip_tags(message), 
        from_email='studentskiparlament.asss@gmail.com',
        recipient_list=[email_recepient],
        html_message=message,  
        fail_silently=False
    )
    return render(request, 'anketa/email.html')

@login_required(login_url='hostlogin')
def success_mail(request):
    user = request.user
    email_recepient = user.email
    alert_poruka = messages.success(request, f'Sifre za Anketu su poslate na vasu {email_recepient} e-mail adresu.')
    return render(request, 'anketa/email.html', context={
        'alert_poruka': alert_poruka
    })

def vote_submit(request, choices):
    if request.method == 'POST':
        choice_id = request.POST.get(['choice'])
        for choice in choices:
            choice = Izbori.objects.get(pk=choice_id)
            choice.votes =+ 1
            choice.save()
            return HttpResponse('Bravo')


@login_required(login_url='hostlogin')
def host_logout(request):
    logout(request)
    return redirect('hosthomepage')


def available_anketas_for_students(request, *args, **kwargs):
    live_ankete = kwargs.get('ankete', [])
    print("Broj aktivnih anketa:", len(live_ankete))
    print("ID-jevi aktivnih anketa:", live_ankete)

    alert_poruka = None
    try:
        
        najnovije_ankete = Anketa.objects.filter(id__in=live_ankete).order_by('-publish_date')
        paginator = Paginator(najnovije_ankete, 2)  
        page_number = request.GET.get('page')
        najnovije_stranice_anketa = paginator.get_page(page_number)
        if not najnovije_stranice_anketa:
            alert_poruka = messages.info(request, 'Nema aktivnih anketa u ovom trenutku')
        
    except ValueError:
        alert_poruka = messages.info(request, 'Desila se greška.')
    
    return render(request, 'anketa/studentviewforvoting.html', context={
        'najnovije_stranice_anketa': najnovije_stranice_anketa,
        'paginator': paginator,  
        'alert_poruka': alert_poruka
    })





def can_students_code_vote_checker(request, anketa_id):
    anketa = get_object_or_404(Anketa, id=anketa_id)
    print(f'ID Ankete je: {anketa.id}')

    code_for_wrong_anketa_msg = None
    code_doesnt_exist_message = None

    if request.method == 'POST':
        backup_kod = request.POST.get('codetextfield')
        print(backup_kod)    
        try:
            kod = BackUpKod.objects.get(code_value=backup_kod)
            print(f'Kod {kod.code_value} postoji. Da li je koriscen? {kod.is_used}')
            match_check = kod.anketa
            if kod.is_used == False and match_check == anketa:
                print(f'Imate prava, jer je {match_check} = {anketa.pk}')
                return redirect('vote', anketa.id, kod.code_value)
            elif kod.is_used == True and match_check == anketa:
                print(f'Imate prava, jer je {match_check} = {anketa.pk}')
                code_is_already_used_msg = messages.warning(request, 'Ваш код је искоришћен.')
                return render (request, 'anketa/studentviewforvoting.html', context={
                                'code_is_already_used_msg': code_is_already_used_msg})
            else:
                print('Nemate prava')
                code_for_wrong_anketa_msg = messages.warning(request, 'Ваш код не одговара овој Анкети, покушајте поново.')
                return render (request, 'anketa/studentviewforvoting.html', context={
                                'code_for_wrong_anketa_msg': code_for_wrong_anketa_msg})
        except BackUpKod.DoesNotExist:
            print('Ne postoji takav kod') 
            code_doesnt_exist_message = messages.error(request, 'Ваш код је не постоји, покушајте поново.') 
    else:
        return HttpResponse('Not a POST method')
    
    return render(request, 'anketa/studentviewforvoting.html', context={
        'anketa': anketa,
        'code_for_wrong_anketa_msg': code_for_wrong_anketa_msg,
        'code_doesnt_exist_message': code_doesnt_exist_message,
        })




def vote(request, anketa_id, kod_value):
    anketa = get_object_or_404(Anketa, pk=anketa_id)
    anketa_name = anketa.naziv
    pitanje = Pitanja.objects.filter(anketa__id=anketa.id).first()
    kod = BackUpKod.objects.filter(code_value=kod_value).first()
    
    if not pitanje:
        raise Http404('Pitanje ne postoji')

    izbori = Izbori.objects.filter(question=pitanje)

    if request.method == 'POST':
        form = VotesForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('forma je validna')
            for izbor in izbori:
                choice_id = request.POST.get(f'vote_{izbor.id}')
                print(f'glas {choice_id} za {izbor.id}')
        
                try:
                    izbor_obj = Izbori.objects.get(pk=izbor.id)
                    print('nije default')
                    vote = Vote(choice=izbor_obj, kod_value=kod, votes=choice_id)
                    if kod.is_used == False:
                        vote.save()
                    else:
                        print('Kod je iskoriscen')  
                        messages.error(request, 'Код je већ искоришћен')  
                except Izbori.DoesNotExist:
                    print(f'Izbori with id {choice_id} does not exist.')
            kod.is_used = True
            kod.save()        
             
            messages.success(request, 'Успешно сте гласали!')
            print(f'Da li je kod {kod.code_value} iskoriscen: {kod.is_used}')
            return render(request, 'anketa/hvalanaglasanju.html', context={'form': form})
        else:
            messages.error(request, 'Došlo je do greške prilikom glasanja.')
    else:
        form = VotesForm()

    return render(request, 'anketa/studentglasa.html', context={
        'anketa': anketa,
        'anketa_name': anketa_name,
        'pitanje': pitanje,
        'izbori': izbori,
        'form': form,
        'kod': kod
    })





def anketa_voting_activity(request):
    ankete = Anketa.objects.all()
    count_ankete = ankete.count()
    print(f'Od ukupno {count_ankete} anketi')
    live_ankete = 0
    finished_ankete = 0
    lista_anketa_koje_ostaju_live = []

    today_date = timezone.now()
    naive_today_date = make_naive(today_date)
    tip = isinstance(today_date, date)
    print(f'Danasnji datum je: {today_date} i tip je date?: {tip}')

    for anketa in ankete:
        duration_time = anketa.vreme_do
        activity_monitoring = duration_time > timezone.make_aware(naive_today_date, timezone.get_current_timezone())
        if anketa.aktivnost and activity_monitoring:  # Direktna provera istinitosti
            live_ankete += 1
            print(f'Ima {live_ankete} aktivnih anketi za studente, + {anketa.id}')
            lista_anketa_koje_ostaju_live.append(anketa.id)
        elif anketa.aktivnost and duration_time < timezone.make_aware(naive_today_date, timezone.get_current_timezone()):
            anketa.aktivnost = False
            anketa.save()        
        else:
            finished_ankete += 1
            print(f'Za anketu {anketa.id} sumiraju se rezultati')

    print(f'Live anketi ima: {live_ankete}')
    print(f'Anketi za ocenjivanje ima: {finished_ankete} tj. gotove su')
    print('Tip je date', isinstance(duration_time, date))

    return redirect('available_anketas_for_students', ankete=lista_anketa_koje_ostaju_live)


# @login_required(login_url='hostlogin')
def rezultati(request):
    obrada_rezultata_zavrsenih_anketi = Anketa.objects.filter(aktivnost=False).all()
    for anketa in obrada_rezultata_zavrsenih_anketi:
        anketa_id = anketa.id
        num_of_students = anketa.broj_kodova
        izbori = Izbori.objects.filter(question_id__anketa_id=anketa_id).values_list('id', flat=True)
        print(f'Anketa sa ID: {anketa_id} je imala {num_of_students} studenta i ima izbore {izbori}')
        for izbor in izbori:
           glasovi_za_izbor = Vote.objects.filter(choice=izbor).values_list('votes', flat=True)
           print(f'Glasovi za izbor {izbor}: {list(glasovi_za_izbor)} na anketi br {anketa_id}')
    


    return HttpResponse('Result')
    

    
# def anketa_voting_activity(request):
    
#     ankete = Anketa.objects.all()
#     count_ankete = ankete.count()
#     print(f'Od ukupno {count_ankete} anketi')
#     live_ankete = 0
#     finished_ankete = 0

#     anketa_activity = True

#     today_date = timezone.now()
#     naive_today_date = make_naive(today_date)
#     tip = isinstance(today_date, date)
#     print(f'Danasnji datum je: {today_date} i tip je date?: {tip}')
    
#     for anketa in ankete:
#         duration_time = anketa.vreme_do
#         print('Tip je date', isinstance(duration_time, date))
#         if anketa.aktivnost == True:
#             activity_monitoring = duration_time < timezone.make_aware(naive_today_date, timezone.get_current_timezone())
#             if activity_monitoring:
#                 while activity_monitoring:
#                     anketa_activity = True
#                     print(f'Vreme isteka ankete ID: {anketa.id} {duration_time} je manje od danasnjeg dana {today_date}. Anketa bi trebala da bude live')
#                     # ovde zelim da za ankete koje su Aktivnost = True i vreme_do(duration_time) manje od danasnjeg dana prikazujem studentima  available_anketas_for_students() metodom
#                     #  npr return redirect(available_anketas_for_students(anketa.id))
#                     if not activity_monitoring:
#                         anketa_activity == False
#                         anketa.aktivnost == False
#                         anketa.save()
#             live_ankete += 1
#         else:
#             finished_ankete += 1
#             # za ankete koje su finished zelim da host-u prikazem rezultate
#             # pozvajuci result() metodu
    
#     print(f'Live anketi ima: {live_ankete}')
#     print(f'Anketi za ocenjivanje ima: {finished_ankete}')



#     lista_anketa_koje_ostaju_live = []

    

    
#     return render(request, 'anketa/anketa_voting_activity', context={
#         'ankete': ankete,
#         'count_ankete': count_ankete,
#         # 'duration_time': duration_time
#         })