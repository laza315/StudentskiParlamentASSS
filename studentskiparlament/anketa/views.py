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
from . models import BackUpKod, Anketa, Pitanja, Izbori
from topics.models import Smer, Profesori, Predmeti
from django.db.models import F
from django.utils.html import strip_tags
from django.core.paginator import Paginator, Page
from time import timezone, time
from datetime import datetime
import time


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

from django.core.paginator import Paginator

def available_anketas_for_students(request):
    alert_poruka = None
    try:
        live_ankete = Anketa.objects.filter(aktivnost=True).all()
        anketa = live_ankete.order_by('-publish_date')
        paginator = Paginator(anketa, 2)  
        page_number = request.GET.get('page')
        najnovije_ankete = paginator.get_page(page_number)
        if not najnovije_ankete:
            alert_poruka = messages.info(request, 'Nema aktivnih anketa u ovom trenutku')
        
    except ValueError:
        alert_poruka = messages.info(request, 'Desila se greska.')
    return render(request, 'anketa/studentviewforvoting.html', context={
        'najnovije_ankete': najnovije_ankete,
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
                code_is_already_used_msg = messages.warning(request, 'Ваш код је већ искоришћен.')
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
    broj_studenata = anketa.broj_kodova
    pitanje = Pitanja.objects.filter(anketa__id=anketa.id).first()
    print(pitanje.question_text)
    kod = BackUpKod.objects.filter(code_value=kod_value).first()
    print(f'Kod je: {kod_value}.')
    print(kod.code_value)
    if not pitanje:
        raise Http404('Pitanje ne postoji')

    izbori = Izbori.objects.filter(question=pitanje)

    if request.method == 'POST':
        for izbor in izbori:
            choice_id = request.POST.get(f'vote_{izbor.id}')
            if choice_id:
                izbor.votes = int(choice_id)
                print('proslo')
                izbor.votes += int(choice_id)
                izbor.save()
                print('Glas je uspešno dodat!')
                
                        
        return HttpResponse('Hvala na glasanju!')

    form = VotesForm()
    return render(request, 'anketa/studentprosao.html', context={
        'anketa': anketa,
        'anketa_name': anketa_name,
        'pitanje': pitanje,
        'izbori': izbori,
        'form': form,
        'kod': kod
    })









# def anketa_voting_activity(request, anketa_id):
    
#     anketa = get_object_or_404(Anketa, anketa_id=id)
#     duration_time = anketa.vreme_do

#     anketa_activity = True

#     today_date = datetime.now()
#     dt_string_frame = today_date.strftime("%d/%m/%Y %H:%M:%S")

#     while anketa_activity:
#         if duration_time < dt_string_frame:
#             print("aktivna")
#         else:
#             anketa_activity = False
#             raise anketa.DoesNotExist

