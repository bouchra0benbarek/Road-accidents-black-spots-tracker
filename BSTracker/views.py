# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.shortcuts import render

# # Create your views here.



from itertools import count
from multiprocessing import context
from operator import imod
import re
from unittest import result
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pytz import timezone
from .models import BlackSpot, caneva, wilaya, report
from .forms import BlackSpotForm
from django.db.models import Sum
from django.utils import timezone
from django.utils.safestring import mark_safe 
from django.utils.html import escapejs
import json

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch




def loginPage(request):
    # page = 'login'
    # if request.user.is_authenticated:
    #     return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {}
    return render(request, 'BSTracker/login_page.html', context)

def logoutUser(request):
    logout(request)
    context = {}
    return redirect('login')
    


def displayListCaneva(request):
    ListCanevas = caneva.objects.all()
    wilayas= wilaya.objects.all()
    return render(request, 'BSTracker/caneva_component.html', {'wilayas': wilayas,'canevas': ListCanevas})

def displayCaneva(request,id):
    caneva_to_display = BlackSpot.objects.filter(caneva_id = id)
    caneva_info = caneva.objects.get(id_caneva = id)
    total_accidents = caneva_to_display.aggregate(Sum('nb_accidents'))
    total_tues = caneva_to_display.aggregate(Sum('nb_tues'))
    total_blesses = caneva_to_display.aggregate(Sum('nb_blesses'))
    total_PN =  caneva_to_display.count() 
    return render(request, 'BSTracker/caneva.html', {'caneva':caneva_to_display, 'caneva_info': caneva_info, 'total_accidents':total_accidents, 'total_tues':total_tues, 'total_blesses':total_blesses, 'total_PN':total_PN})


def displaymap(request):
    wilayas = wilaya.objects.all()
    ListPN = BlackSpot.objects.all()
    map_bs = [{'loc':[pn.lat, pn.lon], 'point_noir': pn.point_noir, 'commune':pn.commune, 
    'nb_acc':pn.nb_accidents, 'nb_tues':pn.nb_tues, 'nb_blesses':pn.nb_blesses} for pn in ListPN]
    canevas = caneva.objects.all()
    listAllCaneva = caneva.objects.all()
    listwilayasent = []
    for i in listAllCaneva:
        w = wilaya.objects.filter(name_wilaya = i.wilaya)[0] 
        if w not in listwilayasent : 
            listwilayasent.append(w)
    

    # map_acc = [{'total_acc':BlackSpot.objects.filter(caneva_id = c.id_caneva).aggregate(Sum('nb_accidents')), 'loc':[wilaya.objects.get(name_wilaya = c.wilaya).lat, wilaya.objects.get(name_wilaya = c.wilaya).lon]} for c in canevas ]
    map_acc = [{'total_acc':caneva.objects.filter(wilaya =w.getName()).aggregate(Sum('total_acc'))['total_acc__sum'], 'loc':[wilaya.objects.get(name_wilaya = w.getName()).lat, wilaya.objects.get(name_wilaya = w.getName()).lon]}for w in listwilayasent]
    context={
            'ListPN':ListPN,
            'map_bs':mark_safe(escapejs(json.dumps(map_bs))),
            'map_acc':mark_safe(escapejs(json.dumps(map_acc))),
            'wilayas':wilayas,
        
    }
    return render(request, 'BSTracker/map.html', context)


def displaydashboard(request):
    ListWilaya = wilaya.objects.all()
    ListCaneva = caneva.objects.filter(year = 2022)
    listAllCaneva = caneva.objects.all()
    listwilayasent = []
    for i in listAllCaneva:
        w = wilaya.objects.filter(name_wilaya = i.wilaya)[0] 
        if w not in listwilayasent : 
            listwilayasent.append(w)
    
    ListPN_Wilaya = [{'x': w.getName(), 'y': caneva.objects.filter(wilaya =w.getName()).aggregate(Sum('total_PN'))['total_PN__sum']} for w in listwilayasent]
    List_Acc_Wilaya = [{'x': w.getName(), 'y':caneva.objects.filter(wilaya =w.getName()).aggregate(Sum('total_acc'))['total_acc__sum']} for w in listwilayasent]
    List_dead_Wilaya = [{'x': w.getName(), 'y':caneva.objects.filter(wilaya =w.getName()).aggregate(Sum('total_dead'))['total_dead__sum']} for w in listwilayasent]
    List_injuries_Wilaya = [{'x': w.getName(), 'y':caneva.objects.filter(wilaya =w.getName()).aggregate(Sum('total_injured'))['total_injured__sum']} for w in listwilayasent]
    years = [2019, 2020, 2021, 2022]
    listPNperYear = [{'x':y,'y':caneva.objects.filter(year = y).aggregate(Sum('total_PN'))["total_PN__sum"]} for y in years]
    total_PN = BlackSpot.objects.count()
    total_acc = caneva.objects.aggregate(Sum('total_acc'))
    total_pn_wilaya = caneva.objects.filter()
    total_dead = caneva.objects.aggregate(Sum('total_dead'))
    total_injured = caneva.objects.aggregate(Sum('total_injured'))
    context={
        'totalPN' : total_PN,
        'total_acc' : total_acc,
        'total_dead': total_dead,
        'total_injured' : total_injured,
        'listPN_wialya' : mark_safe(escapejs(json.dumps(ListPN_Wilaya))),
        'listAcc_wialya' : mark_safe(escapejs(json.dumps(List_Acc_Wilaya))),
        'listDead_wialya' : mark_safe(escapejs(json.dumps(List_dead_Wilaya))),
        'listInjuries_wialya' : mark_safe(escapejs(json.dumps(List_injuries_Wilaya))),
        'listPNperYear' : mark_safe(escapejs(json.dumps(listPNperYear))),
        'wilayas' : ListWilaya
      
    }
    return render(request, 'BSTracker/dashboard.html', context)

def addnewblackspot(request,id, stateName):
    w = wilaya.objects.get(name_wilaya = stateName)
    loc = {"lat":wilaya.objects.get(name_wilaya = stateName).lat, "lon":wilaya.objects.get(name_wilaya = stateName).lon}
    if request.method=='POST':
        c = BlackSpot()
        c.point_noir = request.POST.get('Pname')
        c.commune = request.POST.get('Pcommune')
        c.localisation = request.POST.get('Plocalisation')
        c.valeur_pk = request.POST.get('Ppkvalue')
        c.nb_accidents = request.POST.get('Pnbaccidents')
        c.nb_tues = request.POST.get('Pnbdead')
        c.nb_blesses = request.POST.get('Pnbinjured')
        c.causes = request.POST.get('causes')
        c.mesures = request.POST.get('Pmesures')
        c.observations = request.POST.get('Premarks')
        c.gps = 12.34567
        c.lat = request.POST.get('latitude')
        c.lon = request.POST.get('longitude')
        c.images = request.FILES['image']
        c.caneva_id_id = id
        c.save()
        return redirect('add-new', id = id)
    return (render(request, 'BSTracker/new_black_spot_form.html', {'loc':mark_safe(escapejs(json.dumps(loc)))}))


def createnewcaneva(request,id): 
    wilayas = wilaya.objects.all()
    if request.method=='POST':
        r = caneva.objects.get(id_caneva = id)
        r.wilaya = request.POST.get('selectedValue')
        r.trimestre = request.POST.get('trimestre')
        r.year = request.POST.get('year')
        r.title = 'Caneva de traitement des points noirs de la wilaya ' + r.wilaya
        r.total_acc = BlackSpot.objects.filter(caneva_id = id).aggregate(Sum('nb_accidents'))['nb_accidents__sum']
        r.total_dead = BlackSpot.objects.filter(caneva_id = id).aggregate(Sum('nb_tues'))['nb_tues__sum']
        r.total_injured = BlackSpot.objects.filter(caneva_id = id).aggregate(Sum('nb_blesses'))['nb_blesses__sum']
        r.total_PN = BlackSpot.objects.filter(caneva_id = id).count()
        r.save()
        return redirect('List-caneva')
    ListPN = BlackSpot.objects.filter(caneva_id = id)
    total_PN = ListPN.count()
    total_accidents = ListPN.aggregate(Sum('nb_accidents'))
    total_tues = ListPN.aggregate(Sum('nb_tues'))
    total_blesses = ListPN.aggregate(Sum('nb_blesses'))
    return render(request, 'BSTracker/newcaneva.html', {'id': id,'wilayas':wilayas,'caneva':ListPN, 'total_accidents':total_accidents, 'total_tues':total_tues, 'total_blesses':total_blesses, 'total_PN':total_PN})

def canevasubmitted(request, id):
    if request.method == 'POST':
        r = caneva.objects.get(id_caneva = id)
        r.wilaya = request.POST.get('selectedValue')
        r.save()
    return redirect('List-caneva')


def addnewcaneva(request):
    new_caneva = caneva()
    new_caneva.id_caneva = caneva.objects.count() + 1
    new_caneva.wilaya = ""
    new_caneva.year = 2022
    new_caneva.trimestre = 1
    new_caneva.title = "title2"
    new_caneva.save()
    
    return redirect('add-new', id= new_caneva.id_caneva)

def deletebs(request, id):
    c = BlackSpot.objects.get(id = id)
    id_caneva = c.caneva_id
    c.delete()
    ListPN = BlackSpot.objects.filter(caneva_id = id_caneva)
    total_accidents = BlackSpot.objects.aggregate(Sum('nb_accidents'))
    total_tues = BlackSpot.objects.aggregate(Sum('nb_tues'))
    total_blesses = BlackSpot.objects.aggregate(Sum('nb_blesses'))
    return render(request, 'BSTracker/newcaneva.html', {'caneva':ListPN, 'total_accidents':total_accidents, 'total_tues':total_tues, 'total_blesses':total_blesses})

def editbs(request,id):
    c = BlackSpot.objects.get(id = id)
    form = BlackSpotForm(instance = c)
    if request.method=='POST':
        c.point_noir = request.POST.get('Pname')
        c.commune = request.POST.get('Pcommune')
        c.localisation = request.POST.get('Plocalisation')
        c.valeur_pk = request.POST.get('Ppkvalue')
        c.nb_accidents = request.POST.get('Pnbaccidents')
        c.nb_tues = request.POST.get('Pnbdead')
        c.nb_blesses = request.POST.get('Pnbinjured')
        c.causes = request.POST.get('Pcause')
        c.mesures = request.POST.get('Pmesures')
        c.observations = request.POST.get('Premarks')
        c.gps = 12.34567
        c.save()
    ListPN = BlackSpot.objects.all()
    return render(request, 'BSTracker/newcaneva.html', {'form':form,'caneva':ListPN})

# def showbs(request, id):
#     blackspot = caneva.objects.get(id = id)
#     ListPN = caneva.objects.all()
#     return render(request, 'BSTracker/newcaneva.html', {'blackspot':blackspot, 'caneva':ListPN })

def Displayprofil(request):
    return render(request, 'BSTracker/profil.html')  

def displayReports(request):
      return render(request, 'BSTracker/reports.html')  

def generateNewReport(request, id):
    selected_wilaya =  request.POST.get('wilaya')
    selected_trim =  request.POST.get('trimestre')
    selected_year =  request.POST.get('year')
    id_can = caneva.objects.get(wilaya = selected_wilaya, year = selected_year, trimestre = selected_trim).id_caneva
    
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    venues = caneva.objects.get(id_caneva = id_can)
    textob = p.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # Create blank list
    lines = []
    
    for venue in venues:
        lines.append(venue.title)
        lines.append(" ")

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish Up
    p.drawText(textob)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='hello.pdf')
    
        
    # return render(request, 'BSTracker/newreport.html')  

def newReport(request):
    r = report()
    r.id_report =report.objects.count()+1
    r.report_title = "title"
    # r.save()
    wilayas = wilaya.objects.all()
    return render(request, 'BSTracker/newreport.html', {"id":r.id_report, "wilayas": wilayas})










def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output= ','.join([q.question_text for q in latest_question_list])
    # template = loader.get_template('BSTracker/index.html')
    # context = {'latest_question_list':latest_question_list}
    # return HttpResponse(template.render(context, request))
    # return render(request, 'BSTracker/index.html', context)
    return(render(request, 'BSTracker/login_page.html'))

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist: 
#         raise Http404("Question doens't exist, please try again")
#     return render(request, 'BSTracker/detail.html', {'question': question})

# def results(request, question_id):
#     # response = "u're looking at the question %s"
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'BSTracker/results.html',{'question': question})

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     # try:
#     #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     # except (KeyError, Choice.DoesNotExist):
#     #     # Redisplay the question voting form.
#     #     return render(request, 'BSTracker/detail.html', {
#     #         'question': question,
#     #         'error_message': "You didn't select a choice.",
#     #     })
#     # else:
#     #     selected_choice.votes += 1
#     #     selected_choice.save()
#     #     # Always return an HttpResponseRedirect after successfully dealing
#     #     # with POST data. This prevents data from being posted twice if a
#     #     # user hits the Back button.
#     #     return HttpResponseRedirect(reverse('BSTracker:results', args=(question.id)))
#     return render(request, 'BSTracker/results.html',{'question': question})