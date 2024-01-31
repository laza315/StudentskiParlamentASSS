from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import AnketaForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.mail import send_mail
from .code_generator import CodeGenerator

#Create your views here.

class PasswordsChange(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'anketa/hostprofile.html'
    success_url = reverse_lazy('hostlogin')



def hosthomepage(request):
    obj=User.objects.all()
    hosts = {
        "obj": obj
    }
    return render(request, "anketa/hosthomepage.html", hosts)

@login_required
def profile(request):
    return render(request, 'anketa/hostprofile.html')

@login_required(login_url='login')
def host_makes_anketa(request):
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            anketa = form.save(commit=False)
            anketa.host_id = request.user
            anketa.save()
            print(f'Anketa sa id: {anketa.id},  je uspesno napravljena')

            codes = CodeGenerator.generate_codes()
            mail_bkcodes_sender(request, codes, anketa.id)
            messages.success(request, 'Anketa created successfully!')
            return redirect('email')
        else:
            messages.error(request, 'error ocured')
    else:
        form = AnketaForm()

    context = {'form': form}
    return render(request, 'anketa/anketa.html', context)

@login_required
def mail_bkcodes_sender(request, number_of_codes, anketa_id):
    user = request.user
    email_recepient = user.email
    # print(email_recepient)
    send_mail (
        subject='Hej, ovo je Akademija',
        message= f"Postovani, U prilogu se nalazi lista back_up kodova za Vase studente za anketu pod brojem {anketa_id} : \n".join(number_of_codes),
        from_email='studentskiparlament.asss@gmail.com',
        recipient_list=[email_recepient],
        fail_silently=False
    )
    return render(request, 'anketa/email.html')

def success_mail(request):
    return render(request, 'anketa/email.html')




def host_logout(request):
    logout(request)
    return redirect('hosthomepage')


