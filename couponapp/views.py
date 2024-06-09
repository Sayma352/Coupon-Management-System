import re
from unittest import findTestCases
import json
import datetime
from decimal import Decimal
from urllib import response
from io import BytesIO
from django.utils.html import strip_tags
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.template.loader import get_template,render_to_string
from django.views import View
from xhtml2pdf import pisa
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.db import IntegrityError
from django.contrib import messages
import json
import random
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group,User
from .models import *
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login')
def home(request):
    print(request.user)
    current=datetime.datetime.now()
    return render(request,'home.html')
def menu(request):
    flag=0
    managerNaki=0
    user=None
    if Provost.objects.filter(email=request.user.email):
        user=Provost.objects.get(email=request.user.email)
    elif Manager.objects.filter(email=request.user.email):
        user=Manager.objects.get(email=request.user.email)
        managerNaki=1
    elif Student.objects.filter(email=request.user.email):
        user=Student.objects.get(email=request.user.email)
    if 'feast' in request.POST:
        ss='/payment/'+str(request.POST.get('feast'))
        return redirect(ss)
    if 'menu' in request.POST:
        if managerNaki==0:
         ss='/indMenu/'+str(request.POST.get('menu'))
         return redirect(ss)
        else:
            ss='/managerMenu/'+str(request.POST.get('menu'))
            return redirect(ss)
    if 'breakfast' in request.POST:
        flag=0
        hall=Hall.objects.get(name=user.hall.name)
        menu=Shift.objects.get(name="Breakfast")
        cards=Menu.objects.filter(hall=hall,menuType=menu)
        cont={
            'flag':flag,
            'menu':cards,
            'manager':managerNaki
        }
        return render(request,'menu.html',cont)
    if 'lunch' in request.POST:
        flag=1
        hall=Hall.objects.get(name=user.hall.name)
        menu=Shift.objects.get(name="Lunch")
        cards=Menu.objects.filter(hall=hall,menuType=menu)
        cont={
            'flag':flag,
            'menu':cards,
            'manager':managerNaki
        }
        return render(request,'menu.html',cont)
    if 'dinner' in request.POST:
        flag=2
        current=datetime.date.today()
        boi=False
        feast=Feast.objects.filter()
        ui=None
        hall=Hall.objects.get(name=user.hall.name)
        menu=Shift.objects.get(name="Dinner")
        cards=Menu.objects.filter(hall=hall,menuType=menu)
        for i in feast:
            if i.date==current and i.hall==hall:
                ui=i
                boi=True
        cont=None
        hoise=False
        if boi is False:
         cont={
             'flag':flag,
             'menu':cards,
             'manager':managerNaki,
             'feastNaki':boi
 
         }
        else:
            if managerNaki==1:
                cont={
                    'flag':flag,
                    'feastNaki':boi,
                    'hoise':True,
                    'feast':ui
                }
            else:
               feast=Feast.objects.get(feastId=ui.feastId)
               user=Student.objects.get(email=request.user.email)
               hall=Hall.objects.get(name=user.hall.name)
               ic=feastCoupon.objects.filter(email=request.user.email,
                                         feast=feast,hall=hall)
               if ic:
                   hoise=True
               cont={
                   'flag':flag,
                   'feast':ui,
                   'feastNaki':boi,
                   'hoise':hoise
               }
        return render(request,'menu.html',cont)
    hall=Hall.objects.get(name=user.hall.name)
    menu=Shift.objects.get(name="Breakfast")
    cards=Menu.objects.filter(hall=hall,menuType=menu)
    cont={
        'flag':flag,
        'menu':cards,
        'manager':managerNaki

    }
    return render(request,'menu.html',cont)
def contact(request):
    return render(request,'contact.html')
def logOut(request):
    logout(request)
    return redirect('/login')
def indMenu(request,id):
    menu=Menu.objects.get(menuId=id)
    hall=Hall.objects.get(name=menu.hall.name)
    shift=Shift.objects.get(name=menu.menuType.name)
    addons=AddOns.objects.filter(hall=hall,shift=shift)
    if 'cart' in request.POST:
        cc=couponMenu.objects.filter(email=request.user.email,hall=hall,shift=shift,menu=menu,processed=0)
        if not cc:
            ia=couponMenu(
                email=request.user.email,
                hall=hall,
                shift=shift,
                menu=menu,
                qt=1,
            )
            ia.save()
        else:
         cd=couponMenu.objects.get(email=request.user.email,hall=hall,shift=shift,menu=menu,processed=0)
         cd.qt+=1
         cd.save()
        for o in addons:
            if int(request.POST.get(str(o.addOnId)))>0:
                kire=couponAdd.objects.filter(email=request.user.email,hall=hall,shift=shift,
                              addOn=AddOns.objects.get(hall=hall,shift=shift,addOnId=o.addOnId),processed=0)
                if not kire:
                 ib=couponAdd(
                     email=request.user.email,
                     hall=hall,shift=shift,
                     addOn=AddOns.objects.get(hall=hall,shift=shift,addOnId=o.addOnId),
                 )
                 ib.save()
                 ib.qt+=int(request.POST.get(str(o.addOnId)))
                 ib.save()
                else:
                    kii=couponAdd.objects.get(email=request.user.email,hall=hall,shift=shift,
                            addOn=AddOns.objects.get(hall=hall,shift=shift,addOnId=o.addOnId) ,processed=0)
                    kii.qt+=int(request.POST.get(str(o.addOnId)))
                    kii.save()
        messages.success(request,'Added to order successfully!',extra_tags='hudai')
    cont={
        'add':addons,
        'ui':menu
    }
    return render(request,'indMenu.html',cont)
def logIn(request):
    if 'login' in request.POST:
        if request.POST['type']=='1':
            std=Student.objects.filter(email=request.POST.get('email'))
            if not std or std[0].username is None:
                messages.error(request,'Account Does not Exist',extra_tags='painai')
            else:
                stud=Student.objects.get(email=request.POST.get('email'))
                if stud.request==1:
                    messages.error(request,'Request is waiting to be approved',extra_tags='approve')
                elif stud.password==request.POST.get('pass'):
                    today=datetime.datetime.now().year
                    cc=Student.objects.get(email=request.POST.get('email')).session
                    if int(today)-int(cc)>5:
                        messages.error(request,'Session is expired!',extra_tags='session')
                    else:
                        login(request,authenticate(request,username=stud.username,email=stud.email,password=stud.password))
                        return redirect('/')
                else:
                    messages.error(request,'Passwords do not match!',extra_tags='painai')
        if request.POST['type']=='2':
            prov=Provost.objects.filter(email=request.POST.get('email'))
            if not prov or prov[0].username is None:
                messages.error(request,'Account Does Not Exist',extra_tags='painai' )
            else:
                provo=Provost.objects.get(email=request.POST.get('email'))
                if provo.password==request.POST.get('pass'):
                    login(request,authenticate(request,username=provo.username,email=provo.email,password=provo.password))
                    return redirect('/')
                else:
                    messages.error(request,'Passwords do not match !',extra_tags='painai')
        if request.POST['type']=='3':
            print('okkok')
            manag=Manager.objects.filter(email=request.POST.get('email'))
            if not manag or manag[0].username is None:
                messages.error(request,'Account Does Not Exist',extra_tags='painai' )
            else:
                maa=Manager.objects.get(email=request.POST.get("email"))
                halls=Hall.objects.filter()
                dudu=False
                for o in halls:
                    mm=Manager.objects.get(email=o.manager.email)
                    if mm==maa:
                        dudu=True
                print(dudu)
                if dudu is False:
                    messages.error(request,'User is not associated with any Hall !',extra_tags='painai')
                elif maa.password==request.POST.get('pass'):
                    login(request,authenticate(request,username=maa.username,email=maa.email,password=maa.password))
                    return redirect('/')
                else:
                    messages.error(request,'Passwords do not match !',extra_tags='painai')

    return render(request,'login.html')
def signUp(request):
    dept=Department.objects.filter()
    hall=Hall.objects.filter()
    if 'signup' in request.POST:
        if request.POST['type']=='1':
            
            # stud=Student.objects.filter(email=request.POST.get('email'))
            # if not stud:
            #     print('pk')
            #     messages.error(request,'Enter a valid email',extra_tags='notFound')
            # else:
            #     print('pk2')
            #     std=Student.objects.get(email=request.POST.get('email'))
            #     if std.request==2:
            #         messages.error(request,'Account Already Exists',extra_tags='painai')
            #     elif std.request==1:
            #         messages.error(request,'Wait till Request gets approved',extra_tags='io')
            #     else:
            #         std.username=request.POST.get('user')
            #         std.password=request.POST.get('pass')
            #         std.request=1
            #         std.save()
            #         messages.error(request,'Wait till request gets approved',extra_tags='io')
            stud=Student.objects.filter(email=request.POST.get('email'))
            if not stud:
                ia=Student(
                    name=request.POST.get('name'),
                    studentId=request.POST.get('id'),
                    session=request.POST.get('session'),
                    department=Department.objects.get(name=request.POST.get('dept')),
                    hall=Hall.objects.get(name=request.POST.get('hall')),
                    email=request.POST.get('email'),
                    username=request.POST.get('user'),
                    password=request.POST.get('pass'),
                    request=1
                )
                ia.save()
                messages.error(request,'Wait till request gets approved',extra_tags='io')
            elif stud[0].request==1:
                messages.error(request,'Wait till Request gets approved',extra_tags='io')
            elif stud[0].request==2:
                messages.error(request,'Account Already Exists',extra_tags='painai')
            

        if request.POST['type']=='2':
            provost=Provost.objects.filter(email=request.POST.get('email'))
            if not provost:
                messages.error(request,'Enter a valid email',extra_tags='notFound')
            else:
                prov=Provost.objects.get(email=request.POST.get('email'))
                if prov.username is not None :
                    messages.error(request,'Account Already Exists!',extra_tags='painai')
                else:
                 prov.username=request.POST.get('user')
                 prov.password=request.POST.get('pass')
                 prov.save()
                 user=User.objects.create_user(username=request.POST.get('user'),email=request.POST.get('email'),password=request.POST.get('pass'))
                 messages.success(request,'Account Created Successfully!',extra_tags='ok')
        if request.POST['type']=='3':
            manager=Manager.objects.filter(email=request.POST.get('email'))
            if not manager:
                messages.error(request,'Enter a valid email',extra_tags='notFound')
            else:
                manag=Manager.objects.get(email=request.POST.get('email'))
                if manag.username is not None :
                    messages.error(request,'Account Already Exists!',extra_tags='painai')
                else:
                 manag.username=request.POST.get("user")
                 manag.password=request.POST.get('pass')
                 manag.save()
                 user=User.objects.create_user(username=request.POST.get('user'),email=request.POST.get('email'),password=request.POST.get('pass'))
                 messages.success(request,'Account Created Successfully!',extra_tags='ok')
    cont={
        'dept':dept,
        'hall':hall
    }
    return render(request,'signup.html',cont)
def provost(request):
    user=Provost.objects.get(email=request.user.email)
    hall=Hall.objects.get(name=user.hall.name)
    pend=Student.objects.filter(request=1,hall=hall)
    flag=0
    if 'req' in request.POST:
        flag=0
        pendu=Student.objects.filter(request=1,hall=hall)
        print(len(pendu))
        cont={
            'flag':flag,
            'stud':pendu,
            'len':len(pendu)
        }
        return render(request,'provost.html',cont)
    if 'rep' in request.POST:
        flag=1
        cont={'flag':flag,
              'len':len(pend)
              }
        return render(request,'provost.html',cont)
    if 'sth' in request.POST:
        flag=2
        managerAche=1
        if hall.manager is None:
            managerAche=0
        manager=hall.manager
        cont={'flag':flag,'len':len(pend),
              'managerAche':managerAche,
              'manager':hall.manager
              }
        return render(request,'provost.html',cont) 
    if 'addManager' in request.POST:
        if hall.manager is None:
            cc=Manager.objects.filter(
                hall=None,
                email=request.POST.get('email')
            )
            if not cc:
             ia=Manager(
                 name=request.POST.get('name'),
                 staffId=request.POST.get('id'),
                 mobile=request.POST.get('phone'),
                 email=request.POST.get('email')
             )
             ia.save()
             hall.manager=ia
             ia.save()
            else:
                cd=Manager.objects.get(email=request.POST.get('email'),hall=None)
                hall.manager=cd
                hall.save()

        else:
            ia=Manager.objects.get(email=hall.manager.email,hall=hall)
            ia.hall=None
            ia.save()
            cc=Manager.objects.filter(
                hall=None,
                email=request.POST.get('email')
            )
            if not cc:
             iv=Manager(
                 name=request.POST.get('name'),
                 staffId=request.POST.get('id'),
                 mobile=request.POST.get('phone'),
                 email=request.POST.get('email')
             )
             iv.save()
             hall.manager=iv
             hall.save()
            else:
                cd=Manager.objects.get(email=request.POST.get('email'))
                hall.manager=cd
                hall.save()
        
        subject='Assigned As Manager'
        emailerpath='../templates/mail2.html'
        context={'hall':hall.name}
        emailHtml=get_template(emailerpath).render(context)
        email_msg=EmailMessage(subject,emailHtml,settings.EMAIL_HOST_USER,
                  [hall.manager.email])
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        cont={'flag':2,'len':len(pend),
              'managerAche':1,
              'manager':hall.manager
              }
        return render(request,'provost.html',cont)    
    if 'delete' in request.POST:
        std=Student.objects.get(studentId=int(request.POST['delete']),hall=hall)
        std.delete()
        pendu=Student.objects.filter(request=1)
        return redirect('/provost')
    if 'accept' in request.POST:
        std=Student.objects.get(studentId=int(request.POST['accept']),hall=hall)
        std.request=2
        std.save()
        subject='Request approved'
        emailerpath='../templates/mail.html'
        emailHtml=get_template(emailerpath).render()
        email_msg=EmailMessage(subject,emailHtml,settings.EMAIL_HOST_USER,
                  [std.email])
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        user=User.objects.create_user(username=std.username,email=std.email,password=std.password)
        return redirect('/provost')
    cont={
        'flag':flag,
        'stud':pend,
        'len':len(pend)
    }
    return render(request,'provost.html',cont)
def dashboard(request):
    url=None
    if Provost.objects.filter(email=request.user.email):
        url='/provost'
    elif Manager.objects.filter(email=request.user.email):
        url='/manager'
    elif Student.objects.filter(email=request.user.email):
        url='/student'
    return redirect(url)
def manager(request):
    user=Manager.objects.get(email=request.user.email)
    hall=Hall.objects.get(name=user.hall.name)
    flag=0
    fee=Feast.objects.filter(hall=hall)
    form=MenuForm()
    shift=Shift.objects.filter()
    if 'req' in request.POST:
        flag=0
        cont={
            'flag':flag,
            'shift':shift
        }
        return render(request,'manager.html',cont)
    if 'rep' in request.POST:
        flag=1
        cont={
            'flag':flag,
            'feast':fee,
            'shift':shift
        }
        return render(request,'manager.html',cont)
    if 'sales' in request.POST:
        print(request.POST.get('type'))
        labels=[]
        data=[]
        background=[]
        oo=None
        if request.POST.get('type')=='1':
            oo=request.POST.get('date')
            ok=soldMenu.objects.filter(
            date=request.POST.get('date'),
            hall=hall,
            shift=Shift.objects.get(name=request.POST.get('shift')))
            for j in range(len(ok)):
              color = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
              background.append(color)
            for o in ok:
                labels.append(o.menu.name)
                data.append(o.qt)
            
        elif request.POST.get('type')=='2':
            oo=request.POST.get('month')
            month=int(request.POST.get('month')[5:7])
            year=int(str('2')+request.POST.get('month')[1:4])
            oki=soldMenu.objects.filter(
                hall=hall,shift=Shift.objects.get(name=request.POST.get('shift'))
            )
            based={}
            for o in oki:
                based.__setitem__(o.menu.name,0)
            for j in range(len(oki)):
              color = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
              background.append(color)
            for o in oki:
                if o.date.month==month and o.date.year==year:
                    based[o.menu.name]+=o.qt
            for o in based:
                labels.append(o)
                data.append(based[o])
            print(data)
        elif request.POST.get('type')=='3':
            oo=request.POST.get('year')
            year=int(request.POST.get('year'))
            based={}
            oki=soldMenu.objects.filter(
                hall=hall,shift=Shift.objects.get(name=request.POST.get('shift'))
            )
            for o in oki:
                based.__setitem__(o.menu.name,0)
            for j in range(len(oki)):
              color = ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]
              background.append(color)
            for o in oki:
                if o.date.year==year:
                    based[o.menu.name]+=o.qt
            for o in based:
                labels.append(o)
                data.append(based[o])
        cont={
            'flag':2,
            'labels':labels,
            'data':data,
            'date':oo,
            'shift':request.POST.get('shift'),
            'background':background
        }
        return render(request,'manager.html',cont)
    if 'sth' in request.POST:
        flag=2
        cont={
            'flag':flag
        }
        return render(request,'manager.html',cont)
    if 'add' in request.POST:
        ia=Menu(
            menuId=request.POST.get('menuId'),
            hall=hall,
            menuType=Shift.objects.get(name=request.POST.get('menuType')),
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            desc=request.POST.get('desc'),
            image=request.FILES['image']
        )
        ia.save()
        return redirect('/manager')
    if 'addon' in request.POST:
        ia=AddOns(
            addOnId=request.POST.get('id'),
            hall=hall,
            shift=Shift.objects.get(name=request.POST.get('shift')),
            name=request.POST.get('name'),
            price=request.POST.get('price')
        )
        print(ia)
        ia.save()
        return redirect('/manager')
    if 'feast' in request.POST:
        ia=Feast(
            feastId=request.POST.get('id'),
            date=request.POST.get('date'),
            hall=hall,
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            desc=request.POST.get('desc')
        )
        ia.save()
        fee=Feast.objects.filter(hall=hall)
        cont={
            'flag':0,
            'feast':fee,
            'shift':shift
        }
        return render(request,'manager.html',cont)
    if 'delFeast' in request.POST:
        ia=Feast.objects.get(feastId=request.POST.get('delFeast'),hall=hall)
        ia.delete()
        fee=Feast.objects.filter(hall=hall)
        cont={
            'flag':0,
            'feast':fee,
            'shift':shift
        }
        return render(request,'manager.html',cont)
    cont={
        'flag':flag,
        'shift':shift,
        'form':form,
        'hall':hall
    }
    return render(request,'manager.html',cont)
def student(request):
    user=Student.objects.get(email=request.user.email)
    hall=Hall.objects.get(name=user.hall.name)
    cc=indCoupon.objects.filter(
        student=user,
        hall=hall
    ).order_by('-couponId')
    quer={}
    for o in cc:
        quer.__setitem__(o.couponId,[])
    for o in cc:
        quer[o.couponId].append(o)
    ar=[]
    for o in quer:
        aa=[]
        for i in quer[o]:
            aa.append(i)
        ar.append(aa)
    for o in ar:
        for i in o:
            print(type(i))
    cont={
        'cc':ar
    }

    return render(request,'student.html',cont)
def managerMenu(request,id):
    user=Manager.objects.get(email=request.user.email)
    menu=Menu.objects.get(menuId=int(id))
    hall=Hall.objects.filter(name=user.hall.name)
    cont={
        'menu':menu
    }
    if 'cancel' in request.POST:
        return redirect('/menu')
    if 'save' in request.POST:
        menu.name=request.POST.get('name')
        menu.price=request.POST.get('price')
        menu.desc=request.POST.get('desc')
        if request.FILES.get('image'):
         menu.image=request.FILES['image']
        menu.save()
        return redirect('/menu')
    if 'delete' in request.POST:
        menu.delete()
        return redirect('/menu')
    return render(request,'managerMenu.html',cont)
def cart(request):
    ii=Student.objects.filter(email=request.user.email)
    if not ii:
        return redirect('/error')
    std=Student.objects.get(email=request.user.email)
    hall=Hall.objects.get(name=std.hall.name)
    breakfast=Shift.objects.get(name='Breakfast')
    lunch=Shift.objects.get(name="Lunch")
    dinner=Shift.objects.get(name="Dinner")
    order=couponMenu.objects.filter(email=std.email,hall=hall,shift=breakfast,processed=0)
    addo=couponAdd.objects.filter(email=std.email,hall=hall,shift=breakfast,processed=0)
    order1=couponMenu.objects.filter(email=std.email,hall=hall,shift=lunch,processed=0)
    addo1=couponAdd.objects.filter(email=std.email,hall=hall,shift=lunch,processed=0)
    order2=couponMenu.objects.filter(email=std.email,hall=hall,shift=dinner,processed=0)
    addo2=couponAdd.objects.filter(email=std.email,hall=hall,shift=dinner,processed=0)
    breakprice=0
    lunchprice=0
    dinnerprice=0
    for o in order:
        breakprice+=(o.menu.price*o.qt)
    for o in addo:
        breakprice+=(o.addOn.price*o.qt)
    for o in order1:
        lunchprice+=(o.menu.price*o.qt)
    for o in addo1:
        lunchprice+=(o.addOn.price*o.qt)
    for o in order2:
        dinnerprice+=(o.menu.price*o.qt)
    for o in addo2:
        dinnerprice+=(o.addOn.price*o.qt)
    if 'break' in request.POST:
        for o in order:
            oo=couponMenu.objects.get(email=request.user.email,
                                      hall=hall,
                                      shift=breakfast,
                                      menu=Menu.objects.get(menuId=o.menu.menuId),
                                      processed=0
                                      )
            oo.qt=int(request.POST.get(str(o.menu.menuId)))
            if int(request.POST.get(str(o.menu.menuId)))>0:
             oo.save()
            else:
              oo.delete()
        for o in addo:
            oo=couponAdd.objects.get(email=request.user.email,
                                      hall=hall,
                                      shift=breakfast,
                                      addOn=AddOns.objects.get(addOnId=o.addOn.addOnId),
                                      processed=0
                                      )
            oo.qt=int(request.POST.get(str(o.addOn.addOnId)))
            if int(request.POST.get(str(o.addOn.addOnId)))>0:
             oo.save()
            else:
              oo.delete()
        return redirect('/payment/'+str(breakfast.name))
    if 'lunch' in request.POST:
        for o in order1:
            oo=couponMenu.objects.get(email=request.user.email,
                                      hall=hall,
                                      shift=lunch,
                                      menu=Menu.objects.get(menuId=o.menu.menuId),
                                      processed=0
                                      )
            oo.qt=int(request.POST.get(str(o.menu.menuId)))
            if int(request.POST.get(str(o.menu.menuId)))>0:
             oo.save()
            else:
              oo.delete()
        for o in addo1:
            oo=couponAdd.objects.get(email=request.user.email,
                                      hall=hall,
                                      shift=lunch,
                                      addOn=AddOns.objects.get(addOnId=o.addOn.addOnId),
                                      processed=0
                                      )
            oo.qt=int(request.POST.get(str(o.addOn.addOnId)))
            if int(request.POST.get(str(o.addOn.addOnId)))>0:
             oo.save()
            else:
              oo.delete()
        return redirect('/payment/'+str(lunch.name))
    if 'dinner' in request.POST:
        for o in order2:
            oo=couponMenu.objects.get(email=request.user.email,
                                      hall=hall,
                                      shift=dinner,
                                      menu=Menu.objects.get(menuId=o.menu.menuId),
                                      processed=0
                                      )
            oo.qt=int(request.POST.get(str(o.menu.menuId)))
            if int(request.POST.get(str(o.menu.menuId)))>0:
             oo.save()
            else:
              oo.delete()
        for o in addo2:
            oo=couponAdd.objects.get(email=request.user.email,
                                      hall=hall,
                                      shift=dinner,
                                      addOn=AddOns.objects.get(addOnId=o.addOn.addOnId),
                                      processed=0
                                      )
            oo.qt=int(request.POST.get(str(o.addOn.addOnId)))
            if int(request.POST.get(str(o.addOn.addOnId)))>0:
             oo.save()
            else:
              oo.delete()
        return redirect('/payment/'+str(dinner.name))
        
    cont={
        'order':order,
        'addo':addo,
        'order1':order1,
        'addo1':addo1,
        'order2':order2,
        'addo2':addo2,
        'lprice':lunchprice,
        'bprice':breakprice,
        'dprice':dinnerprice
    }
    return render(request,'cart.html',cont)
def payment(request,id):
    cont=None
    total=0
    user=Student.objects.get(email=request.user.email)
    if id!='Breakfast' and id!='Lunch' and id!='Dinner':
        feast=Feast.objects.get(feastId=int(id))
        cont={
            'shift':id,
             'total':feast.price,
             'user':user
        }
        total=feast.price
    else:
     hall=Hall.objects.get(name=user.hall.name)
     shift=Shift.objects.get(name=id)
     order=couponMenu.objects.filter(
         email=user.email,
         hall=hall,
         shift=shift,
         processed=0
     )
     addO=couponAdd.objects.filter(
         email=user.email,
         hall=hall,
         shift=shift,
         processed=0
     )
     for o in order:
         total+=o.qt*o.menu.price
     for o in addO:
         total+=o.qt*o.addOn.price
     if total==0:
         messages.error(request,'Order can not be empty!',extra_tags='empty')
     cont={
         'user':user,
         'total':total,
         'shift':id
     }
    if 'pay' in request.POST:
        if request.POST.get('pay')=='4':
            return redirect('/cart')
        else:
            ss='/notun/'+id+'/'+request.POST.get('pay')+'/'+str(total)
            return redirect(ss)
    return render(request,'payment.html',cont)
def notun(request,id,id2,id3):
    id2=int(id2)
    cont={
        'shift':id,
        'id':id2,
        'total':id3
    }
    return render(request,'notun.html',cont)
def coupon(request,id):
    feastNaki=False
    if id!='Breakfast' and id!='Lunch' and id!='Dinner':
        feastNaki=True
    if 'back' in request.POST:
        if feastNaki is False:
         user=Student.objects.get(email=request.user.email)
         hall=Hall.objects.get(name=user.hall.name)
         shift=Shift.objects.get(name=id)
         total=0
         today=datetime.datetime.now().date()
         order=couponMenu.objects.filter(
             email=user.email,
             hall=hall,
             shift=shift,
             processed=0
         )
         addO=couponAdd.objects.filter(
             email=user.email,
             hall=hall,
             shift=shift,
             processed=0
         )             
         cc=indCoupon.objects.filter()
         ii=len(cc)+1
         for o in order:
             ok=indCoupon(
                 date=today,
                 couponId=ii,
                 hall=hall,
                 couponMenu=o,
                 student=user
             )
             ok.save()
             ia=soldMenu.objects.filter(date=today,hall=hall,shift=shift,menu=Menu.objects.get(menuId=o.menu.menuId))
             if not ia:
                 jj=soldMenu(
                     date=today,
                     shift=shift,
                     hall=hall,
                     menu=Menu.objects.get(menuId=o.menu.menuId),
                     qt=o.qt
                 )
                 jj.save()
             else: 
                 jj=soldMenu.objects.get(
                     date=today,
                     shift=shift,
                     hall=hall,
                     menu=Menu.objects.get(menuId=o.menu.menuId)
                 )
                 jj.qt+=o.qt
                 jj.save()
             oo=couponMenu.objects.get(
                 email=user.email,
                 hall=hall,
                 shift=shift,
                 menu=Menu.objects.get(menuId=o.menu.menuId),
                 processed=0
             )
             oo.processed=1
             oo.save()
         for o in addO:
             ok=indCoupon(
                 date=today,
                 couponId=ii,
                 hall=hall,
                 student=user,
                 couponAdd=o
             )
             ok.save()
             oo=couponAdd.objects.get(
                 email=user.email,
                 hall=hall,
                 shift=shift,
                 addOn=AddOns.objects.get(addOnId=o.addOn.addOnId),
                 processed=0
             )
             oo.processed=1
             oo.save()
        else:
            feast=Feast.objects.get(feastId=int(id))
            user=Student.objects.get(email=request.user.email)
            hall=Hall.objects.get(name=user.hall.name)
            ii=feastCoupon(
                email=request.user.email,
                hall=hall,
                feast=feast
            )
            ii.save()
        return redirect('/')
    if 'gut' in request.POST:
        if feastNaki is False:
         ss='/arekta/'+str(id)
        else:
            ss='/feast/'+str(id)
        return redirect(ss)
    if feastNaki is False:
     current=datetime.datetime.now().hour
     user=Student.objects.get(email=request.user.email)
     hall=Hall.objects.get(name=user.hall.name)
     shift=Shift.objects.get(name=id)
     total=0
     order=couponMenu.objects.filter(
         email=user.email,
         hall=hall,
         shift=shift,
         processed=0
     )
     addO=couponAdd.objects.filter(
         email=user.email,
         hall=hall,
         shift=shift,
         processed=0
     )
     date=None
     kk=indCoupon.objects.filter().order_by('-couponId')
     ii=0
     if kk:
         ii=kk[0].couponId+1
     else:
         ii=1
     today=datetime.datetime.now().date()
     tomorrow=today+datetime.timedelta(days=1)
     session=int(user.session)
     if id=='Dinner':
         if current>=14:
             date=tomorrow
         else:
             date=today
     else:
         date=tomorrow
     for o in order:
         total+=o.qt*o.menu.price
     for o in addO:
         total+=o.qt*o.addOn.price
     cont={
         'id':ii,
         'shift':id,
         'date':date,
         'hall':hall.name,
         'order':order,
         'addO':addO,
         'session':session,
         'user':user,
         'total':total,
         'feastNaki':feastNaki
     }
     return render(request,'coupon.html',cont)
    else:
        feast=Feast.objects.get(feastId=int(id))
        user=Student.objects.get(email=request.user.email)
        session=int(user.session)
        cont={
            'hall':user.hall.name,
            'shift':'Feast',
            'feast':feast,
            'user':user,
            'session':session,
            'total':feast.price,
            'date':feast.date,
            'feastNaki':feastNaki
        }
        return render(request,'coupon.html',cont)
    
def feast_pdf_view(request,id):
    feast=Feast.objects.get(feastId=int(id))
    user=Student.objects.get(email=request.user.email)
    session=int(user.session)
    template_path = 'feast.html'
    context = {
      'hall':user.hall.name,
      'shift':'Feast',
      'feast':feast,
      'user':user,
      'session':session,
      'total':feast.price,
      'date':feast.date,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="coupon.pdf"'
    template = get_template(template_path)
    html = template.render(context)    
    pisa_status = pisa.CreatePDF(
       html, dest=response )
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def render_pdf_view(request,id):
    current=datetime.datetime.now().hour
    user=Student.objects.get(email=request.user.email)
    hall=Hall.objects.get(name=user.hall.name)
    shift=Shift.objects.get(name=id)
    total=0
    order=couponMenu.objects.filter(
        email=user.email,
        hall=hall,
        shift=shift,
        processed=0
    )
    addO=couponAdd.objects.filter(
        email=user.email,
        hall=hall,
        shift=shift,
        processed=0
    )
    date=None
    today=datetime.datetime.now().date()
    tomorrow=today+datetime.timedelta(days=1)
    session=int(user.session)
    if id=='Dinner':
        if current>=14:
            date=tomorrow
        else:
            date=today
    else:
        date=tomorrow
    for o in order:
        total+=o.qt*o.menu.price
    for o in addO:
        total+=o.qt*o.addOn.price
    print('hoy nai')
    template_path = 'arekta.html'
    date=None
    kk=indCoupon.objects.filter().order_by('-couponId')
    ii=0
    if kk:
        ii=kk[0].couponId+1
    else:
        ii=1
    context = {
        'id':ii,
        'shift':id,
        'date':date,
        'hall':hall.name,
        'order':order,
        'addO':addO,
        'session':session,
        'user':user,
        'total':total
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="coupon.pdf"'
    template = get_template(template_path)
    html = template.render(context)    
    pisa_status = pisa.CreatePDF(
       html, dest=response )
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
def error(request):
    return render(request,'error.html')