from django.shortcuts import render
from main_app.forms import StudentUserForm,StudentsInfoForm, LabUserForm, LabInfoForm, BTPUserForm, BTPInfoForm, OtherUserForm, HODUserForm, HODInfoForm, OtherInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from main_app.models import Department, StudentUserInfo, HODUserInfo, LabUserInfo, BTPUserInfo, OtherUserInfo, LabRequests, BTPRequest, OtherRequest, HeavenUserInfo
import datetime
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from main_app.graph_helper import get_user
from main_app.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import smtplib, os, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from noDuesBeta.settings import EMAIL_HOST_USER , EMAIL_HOST_PASSWORD
from django.core.mail import EmailMessage

@login_required
def user_logout(request):
    logout(request);
    return HttpResponseRedirect(reverse('mainPage'))

def student_logout(request):
    logout(request)
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('mainPage'))


def send_emailll(recipient,body):
    try:    
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = recipient   
        msg['Subject'] = "NO DUES APPLICATION"
        
        # see the code below to use template as body
        body_text = "This is an auto-generated mail\n"
        body_html = body
        
        # Create the body of the message (a plain-text and an HTML version).
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(body_text, 'plain')
        part2 = MIMEText(body_html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        
        # Send the message via local SMTP server.
        
        mail = smtplib.SMTP("smtp.outlook.office365.com", 587, timeout=20)

        # if tls = True                
        mail.starttls()        

        recepient = [recipient]
                    
        mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)        
        mail.sendmail(EMAIL_HOST_USER, recipient, msg.as_string())        
        mail.quit()
        
    except Exception as e:
        raise e

# def send_email(user, pwd, recipient, subject, body):
#     import smtplib

#     FROM = user
#     TO = recipient if isinstance(recipient, list) else [recipient]
#     SUBJECT = subject
#     TEXT = body

#     # Prepare actual message
#     message = """From: %s\nTo: %s\nSubject: %s\n\n%s
#     """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.ehlo()
#         server.starttls()
#         server.login(user, pwd)
#         server.sendmail(FROM, TO, message)
#         server.close()
#         print ('successfully sent the mail')
#     except:
#         print ("failed to send mail")


# def sendd(recipient, body):
#     # sender_email = "my@gmail.com"
#     # receiver_email = "your@gmail.com"
#     # password = input("Type your password and press enter:")
#     message = MIMEMultipart("alternative")
#     message["Subject"] = "NO DUES APPLICATION"
#     message["From"] = EMAIL_HOST_USER
#     message["To"] = recipient

#     # Create the plain-text and HTML version of your message
#     # text = """\
#     # Hi,
#     # How are you?
#     # Real Python has many great tutorials:
#     # www.realpython.com"""
#     # html = """\
#     # <html>
#     #   <body>
#     #     <p>Hi,<br>
#     #        How are you?<br>
#     #        <a href="http://www.realpython.com">Real Python</a> 
#     #        has many great tutorials.
#     #     </p>
#     #   </body>
#     # </html>
#     # """

#     # Turn these into plain/html MIMEText objects
#     #part1 = MIMEText(text, "plain")
#     part2 = MIMEText(body, "html")

#     # Add HTML/plain-text parts to MIMEMultipart message
#     # The email client will try to render the last part first
#     #message.attach(part1)
#     message.attach(part2)

#     # Create secure connection with server and send email
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL("smtp.outlook.office365.com", 465, context=context) as server:
#         server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#         server.sendmail(
#             EMAIL_HOST_USER, recipient, message.as_string()
#         )

def mainPage(request):



    if request.user.is_authenticated:


        dict1 = StudentUserInfo.objects.filter(user=request.user)
        if len(dict1)>0:
            print(dict1)
            context = initialize_context(request)
            if(context['user']['is_authenticated'] == False):
                return user_logout(request)
            return HttpResponseRedirect(reverse('studentIndex'))
        else:
            dict2 = LabUserInfo.objects.filter(user=request.user)
            if len(dict2)>0:
                return HttpResponseRedirect(reverse('labIndex'));
            else:
                dict3 = OtherUserInfo.objects.filter(user=request.user)
                if len(dict3)>0:
                    return HttpResponseRedirect(reverse('otherIndex'))
                else:
                    dict4 = BTPUserInfo.objects.filter(user=request.user)
                    if len(dict4)>0:
                        return HttpResponseRedirect(reverse('btpIndex'))
                    else:
                        dict5 = HODUserInfo.objects.filter(user=request.user)
                        if len(dict5)>0:
                            return HttpResponseRedirect(reverse('hodIndex'))
                        else:
                            return HttpResponse("unable to log in")

    else:

        return render(request, 'main_app/base.html')

def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  print('Request Session', request.session)
  print('contexttt', context)
  if (context['user']['is_authenticated'] == True):
      login(request, StudentUserInfo.objects.get(user__email = context['user']['email']).user)

  return context



def callback(request):
  # Get the state saved in session



  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  try:
    print("Found", StudentUserInfo.objects.get(user__email=user['mail']))
    login(request, StudentUserInfo.objects.get(user__email=user['mail']).user)
  except:
    print(StudentUserInfo.objects.get(user__email='voter@maadr.chod'))

  # Save token and user
  store_token(request, token)
  store_user(request, user)



  return HttpResponseRedirect(reverse('studentIndex'))


def sign_ino(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)

class Entry():
    name = ""
    a=0
    b=0
    c=0

def heavenIndex(request):


    if request.POST:
        print(request.POST)
        # for x in LabUserInfo.objects.all():
        #     c = LabRequests.objects.filter(lab=x,approval_status=0)
        #     if len(c)>0:
        #         mess="Hello "+ x.user.username+ "! You have "+str(len(c))+" requests pending to approve. Kindly approve/reject them at the earliest. Thank You!"
        #         send_emailll(str(x.user.email),mess)
        # for x in OtherUserInfo.objects.all():
        #     c = OtherRequest.objects.filter(other=x,approval_status=0)
        #     if len(c)>0:
        #         mess="Hello "+ x.user.username+ "! You have "+str(len(c))+" requests pending to approve. Kindly approve/reject them at the earliest. Thank You!"
        #         send_emailll(str(x.user.email),mess)
        # for x in BTPUserInfo.objects.all():
        #     c = BTPRequest.objects.filter(btp=x,approval_status=0)
        #     if len(c)>0:
        #         mess="Hello "+ x.user.username+ "! You have "+str(len(c))+" requests pending to approve. Kindly approve/reject them at the earliest. Thank You!"
        #         send_emailll(str(x.user.email),mess)
        for x in HODUserInfo.objects.all():
            c = BTPRequest.objects.filter(btp__department=x.department,approval_status=1)
            C2= LabRequests.objects.filter(lab__department=x.department,approval_status=1)
            C3 = BTPRequest.objects.filter(hod=x,approval_status=1)
            mess="Hello "+ x.user.username+ "!"
            if len(c)+len(C3)>0:
                mess+=" You have "+str(len(c)+len(C3))+" BTP requests pending to approve"
            if len(C2) > 0:
                if(len(c)+len(C3))>0:
                    mess+=" also"
                mess+=" You have "+str(len(C2))+" Lab requests pending to approve"
            if len(c)+len(C2)+len(C3)>0:
                mess+= ". Kindly approve/reject them at the earliest. Thank You!"
                send_emailll(str(x.user.email),mess)



    if request.user.is_authenticated:

        dict2 = HeavenUserInfo.objects.filter(user=request.user)
        if len(dict2) == 0:
            return HttpResponseRedirect(reverse('mainPage'))

        dict = []

        students = StudentUserInfo.objects.all()

        for student in students:
            a=0
            b=0
            c=0
            department = student.department
            labsRequired = LabUserInfo.objects.filter(department__in=[department])
            labsAccepted = LabRequests.objects.filter(student=student, approval_status=2)
            f=0
            temp = []
            if len(labsRequired)>len(labsAccepted):
                a=1

            btpAccepted = BTPRequest.objects.filter(student=student, approval_status = 2)
            if len(btpAccepted)==0:
                b=1

            othersAccepted = OtherRequest.objects.filter(student=student, approval_status = 2)

            if len(othersAccepted)<3:
                c=1

            ent = Entry()
            ent.name = student.rollnumber
            ent.a = a
            ent.b = b
            ent.c = c

            dict.append(ent)

        dict.sort(key=lambda Entry: Entry.name)

        return render(request, 'main_app/heavenIndex.html', {'dict': dict})

    else:
        return HttpResponseRedirect(reverse('mainPage'))


@csrf_exempt
def studentIndex(request):


    if request.POST:

        print('POSTY', request.POST)
        applied=""
        context = initialize_context(request)


        if context['user']['is_authenticated'] == False:
            return user_logout(request)

        print('CONCON', context)

        student = StudentUserInfo.objects.get(user__email=context['user']['email'])
        varlib = request.POST.get('Library/CCC',None)
        if varlib:
            try:
                vlib = OtherRequest.objects.get(student=student, other=OtherUserInfo.objects.get(user__username="LibraryCCC"))
            except:
                vlib = None

            if vlib:
                vlib.delete()
                lib = OtherRequest.objects.create( other=OtherUserInfo.objects.get(user__username="LibraryCCC"),
                                                student=student,
                                                remark="",
                                                date_sent=datetime.date.today(),
                                                approval_status=0
                                                )
                applied += lib.other.user.username+","

            else:
                lib = OtherRequest.objects.create(  other=OtherUserInfo.objects.get(user__username="LibraryCCC"),
                                                student=student,
                                                remark="",
                                                date_sent=datetime.date.today(),
                                                approval_status=0
                                                )
                applied += lib.other.user.username+","

        varlib = request.POST.get('Gymkhana',None)
        if varlib:
            try:
                vlib = OtherRequest.objects.get(student=student, other=OtherUserInfo.objects.get(user__username="Gymkhana"))
            except:
                vlib = None

            if vlib:
                vlib.delete()
                lib = OtherRequest.objects.create(  other=OtherUserInfo.objects.get(user__username="Gymkhana"),
                                                student=student,
                                                remark="",
                                                date_sent=datetime.date.today(),
                                                approval_status=0
                                                )
                applied += lib.other.user.username+","
            else:
                lib = OtherRequest.objects.create(  other=OtherUserInfo.objects.get(user__username="Gymkhana"),
                                                student=student,
                                                remark="",
                                                date_sent=datetime.date.today(),
                                                approval_status=0
                                                )
                applied += lib.other.user.username+","

        varlib = request.POST.get('HOSTEL',None)
        if varlib:
            try:
                vlib = OtherRequest.objects.get(student=student, other=OtherUserInfo.objects.get(user__username=varlib))
            except:
                vlib = None

            if vlib:
                vlib.delete()
                lib = OtherRequest.objects.create(  other=OtherUserInfo.objects.get(user__username=varlib),
                                                student=student,
                                                remark="",
                                                date_sent=datetime.date.today(),
                                                approval_status=0
                                                )
                applied += lib.other.user.username+","
            else:
                lib = OtherRequest.objects.create(  other=OtherUserInfo.objects.get(user__username=varlib),
                                                student=student,
                                                remark="",
                                                date_sent=datetime.date.today(),
                                                approval_status=0
                                                )
                applied += lib.other.user.username+","



        varbtp = request.POST.get('BTP',None)
        if varbtp:
            try:
                btpt = BTPRequest.objects.get(student=student)
            except:
                btpt = None

            try:
                btpOrHod = BTPUserInfo.objects.get(user__username = varbtp)
                approval_status = 0
            except:
                btpOrHod = HODUserInfo.objects.get(user__username = varbtp)
                approval_status = 1


            if btpt:
                btpt.delete()
                if approval_status == 0:
                    btp = BTPRequest.objects.create(  btp=btpOrHod,
                                                    student=student,
                                                    remark="",
                                                    date_sent=datetime.date.today(),
                                                    approval_status=approval_status
                                                    )
                    applied += btp.btp.user.username+","
                else:
                    btp = BTPRequest.objects.create(  hod=btpOrHod,
                                                    student=student,
                                                    remark="",
                                                    date_sent=datetime.date.today(),
                                                    approval_status=approval_status
                                                    )
                    applied += btp.hod.user.username+","

            else:

                if approval_status == 0:
                    btp = BTPRequest.objects.create(  btp=btpOrHod,
                                                     student=student,
                                                     remark="",
                                                     date_sent=datetime.date.today(),
                                                     approval_status=approval_status
                                                     )
                    applied += btp.btp.user.username+","
                else:
                    btp = BTPRequest.objects.create(  hod=btpOrHod,
                                                     student=student,
                                                     remark="",
                                                     date_sent=datetime.date.today(),
                                                     approval_status=approval_status
                                                     )
                    applied += btp.hod.user.username+","






        labs = LabUserInfo.objects.filter(department__in=[student.department],prog=student.prog)
        for lab in labs :
            varlab = request.POST.get(lab.user.username, None)
            if varlab:
                try:
                    ll = LabRequests.objects.get(student=student, lab=LabUserInfo.objects.get(user__username=varlab))
                except:
                    ll = None
                if ll:
                    ll.delete()
                    labx = LabRequests.objects.create(  lab=LabUserInfo.objects.get(id=lab.id),
                                                student=student,
                                                remark="",
                                                date_sent=datetime.date.today(),
                                                approval_status=0
                                                )
                    applied += labx.lab.user.username+","
                else:
                    labx = LabRequests.objects.create(  lab=LabUserInfo.objects.get(id=lab.id),
                                                student=student,
                                                remark="",
                                                date_sent=datetime.date.today(),
                                                approval_status=0
                                                )
                    applied += labx.lab.user.username+","

        labR = LabRequests.objects.filter(student__user=request.user)
        btpR = BTPRequest.objects.filter(student__user=request.user)
        otherR = OtherRequest.objects.filter(student__user=request.user)
        # smtp = smtplib.SMTP('smtp.gmail.com',587)
        # smtp.ehlo()
        # smtp.starttls()
        # smtp.ehlo()
        # smtp.login('ritik.mandloi.2000@gmail.com', 'RM16217717')
        app = []
        app=applied.split(',')
        mess="<html><head><style>"
        mess+="table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 5px;text-align: left;}</style></head><body><h3>YOU HAVE APPLIED FOR THE FOLLOWING : </h3><br><br>"
        mess+="<table><caption>LABS</caption><tr><th>Applied to </th><th>Approval Status </th><th>Remark (If Any)</th></tr>"

        subject="NO DUES APPLICATION"
        useremail=str(request.user.email)
        if(app[-1] == ""):
            app.pop()
        for x in labR:
            mess+="<tr><td>"+str(x.lab.user.username)+"</td><td>"
            if(x.approval_status == 0):
                mess+="Waiting"
            elif(x.approval_status == 1):
                mess+="Waiting for HOD approval"
            elif(x.approval_status == 2):
                mess+="Approved"
            else:
                mess+="Rejected"
            mess+="</td><td>"+str(x.remark)+"</td></tr>"
        mess+="</table><br><table><caption>BTP</caption><tr><th>Applied to </th><th>Approval Status </th><th>Remark (If Any)</th></tr>"
        for x in btpR:
            if(x.btp):
                mess+="<tr><td>"+str(x.btp.user.username)+"</td><td>"
            if(x.hod):
                mess+="<tr><td>"+str(x.hod.user.username)+"</td><td>"
            if(x.approval_status == 0):
                mess+="Waiting"
            elif(x.approval_status == 1):
                mess+="Waiting for HOD approval"
            elif(x.approval_status == 2):
                mess+="Approved"
            else:
                mess+="Rejected"
            mess+="</td><td>"+str(x.remark)+"</td></tr>"
        mess+="</table><br><table><caption>OTHERS</caption><tr><th>Applied to </th><th>Approval Status </th><th>Remark (If Any)</th></tr>"
        for x in otherR:
            mess+="<tr><td>"+str(x.other.user.username)+"</td><td>"
            if(x.approval_status == 0):
                mess+="Waiting"
            elif(x.approval_status == 1):
                mess+="Waiting for HOD approval"
            elif(x.approval_status == 2):
                mess+="Approved"
            else:
                mess+="Rejected"
            mess+="</td><td>"+str(x.remark)+"</td></tr>"
        mess+="</table></body></html>"
        print(mess)

        send_emailll(useremail,mess)
        return HttpResponseRedirect(reverse('mainPage'))



    if request.user.is_authenticated:

        context = initialize_context(request)

        if context['user']['is_authenticated'] == False:
            return user_logout(request)

        print('CONCON', context)




        print('CONTEXT', context)

        labRequests = LabRequests.objects.filter(student__user=request.user)
        btpRequests = BTPRequest.objects.filter(student__user=request.user)
        otherRequests = OtherRequest.objects.filter(student__user=request.user)
        context['labRequests'] = labRequests
        context['btpRequests'] = btpRequests
        context['otherRequests'] = otherRequests

        return render(request, 'main_app/student_main_page.html', context);

    else:

        return HttpResponseRedirect(reverse('mainPage'))

# def send_email(user, pwd, recipient, subject, body):
#     import smtplib

#     FROM = user
#     TO = recipient if isinstance(recipient, list) else [recipient]
#     SUBJECT = subject
#     TEXT = body

#     # Prepare actual message
#     message = """From: %s\nTo: %s\nSubject: %s\n\n%s
#     """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.ehlo()
#         server.starttls()
#         server.login(user, pwd)
#         server.sendmail(FROM, TO, message)
#         server.close()
#         print ('successfully sent the mail')
#     except:
#         print ("failed to send mail")

def labIndex(request):

    p = 0
    if request.POST:
        if 'Accept' in request.POST:
            for req in LabRequests.objects.filter(lab__user=request.user, approval_status=0):
                p = 1
                stud = str(req.student.rollnumber)
                if request.POST.getlist(stud)[0] == 'YES':

                    req.approval_status = 1
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()

        elif 'Reject' in request.POST:
            for req in LabRequests.objects.filter(lab__user=request.user, approval_status=0):
                p = 1
                stud = str(req.student.rollnumber)
                if request.POST.getlist(stud)[0] == 'YES':
                    req.approval_status = 3
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION"
                    mess="Your application for " + str(req.lab.user.username) + " has been REJECTED!\n"
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark
                    mess+="\nKindly pay your dues and apply again!"
                    send_emailll(useremail,mess)

        else:

            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return HttpResponseRedirect(reverse("labIndex"))
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("labIndex"))

            file_data = csv_file.read().decode("utf-8")

            lines = file_data.split("\n")
            lines.pop()
            c = 0
            f = 0
            for line in lines:
                fields = line.split(",")
                if(len(fields) >= 2):
                    if(fields[0].isdigit()):
                        c = c + 1
                        if 'AcceptCSV' in request.POST:
                            for req in LabRequests.objects.filter(lab__user=request.user,student__rollnumber=fields[0],approval_status=0):
                                req.approval_status = 1
                                req.remark = "Approved - "+fields[1]
                                req.save()
                        if 'RejectCSV' in request.POST:
                            for req in LabRequests.objects.filter(lab__user=request.user,student__rollnumber=fields[0],approval_status=0):
                                req.approval_status = 3
                                req.remark = "Rejected - "+fields[1]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.lab.user.username) + " has been REJECTED!"
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                mess+="\nKindly pay your dues and apply again!"
                                send_emailll(useremail,mess)
                else:
                    messages.error(request,'Incorrect File Format!\nEvery Row should have atleast two entries,\nFirst entry being rollnumber and the second being the remark')
                    f = 1
                    break
            if c == 0 and f == 0:
                messages.error(request,'Incorrect File Format!\nEvery Row should have atleast two entries,\nFirst entry being rollnumber and the second being the remark')


        return HttpResponseRedirect(reverse('mainPage'))


    if request.user.is_authenticated:
        dict = LabUserInfo.objects.filter(user=request.user)
        for dic in dict:
            if dic.approval_status == 0:
                return render(request, 'main_app/waiting_page.html')
            else:
                requests = LabRequests.objects.filter(lab__user=request.user, approval_status=0)
                if requests:
                    p = 1
                return render(request, 'main_app/lab_main_page.html', {'requests': requests, 'p' : p});
    return HttpResponseRedirect(reverse('mainPage'))


def btpIndex(request):

    p = 0
    if request.POST:
        if 'Accept' in request.POST:
            for req in BTPRequest.objects.filter(btp__user=request.user, approval_status=0):
                p = 1
                stud = str(req.student.rollnumber)
                if request.POST.getlist(stud)[0] == 'YES':
                    req.approval_status = 1
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()


        elif 'Reject' in request.POST:
            for req in BTPRequest.objects.filter(btp__user=request.user, approval_status=0):
                p = 1
                stud = str(req.student.rollnumber)
                if request.POST.getlist(stud)[0] == 'YES':
                    req.approval_status = 3
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION"
                    mess="Your application for " + str(req.btp.user.username) + " has been REJECTED!"
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark
                    mess+="\nKindly pay your dues and apply again!"
                    send_emailll(useremail,mess)
        else:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return HttpResponseRedirect(reverse("btpIndex"))
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("btpIndex"))

            file_data = csv_file.read().decode("utf-8")

            lines = file_data.split("\n")
            lines.pop()
            c = 0
            f = 0
            for line in lines:
                fields = line.split(",")
                if(len(fields) >= 2):
                    if(fields[0].isdigit()):
                        c = c + 1
                        if 'AcceptCSV' in request.POST:
                            for req in BTPRequest.objects.filter(btp__user=request.user,student__rollnumber=fields[0],approval_status=0):
                                req.approval_status = 1
                                req.remark = fields[1]
                                req.save()
                        if 'RejectCSV' in request.POST:
                            for req in BTPRequest.objects.filter(btp__user=request.user,student__rollnumber=fields[0],approval_status=0):
                                req.approval_status = 3
                                req.remark = fields[1]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.btp.user.username) + " has been REJECTED!"
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                mess+="\nKindly pay your dues and apply again!"
                                send_emailll(useremail,mess)

                else:
                    messages.error(request,'Incorrect File Format!\nEvery Row should have atleast two entries,\nFirst entry being rollnumber and the second being the remark')
                    f = 1
                    break
            if c == 0 and f == 0:
                messages.error(request,'Incorrect File Format!\nEvery Row should have atleast two entries,\nFirst entry being rollnumber, second being  the remark')


        return HttpResponseRedirect(reverse('mainPage'))


    if request.user.is_authenticated:
        dict = BTPUserInfo.objects.filter(user=request.user)
        for dic in dict:
            if dic.approval_status == 0:
                return render(request, 'main_app/waiting_page.html')
            else:
                requests = BTPRequest.objects.filter(btp__user=request.user, approval_status=0)
                if requests:
                    p = 1
                return render(request, 'main_app/btp_main_page.html', {'requests': requests, 'p' : p});

    return HttpResponseRedirect(reverse('mainPage'))

def otherIndex(request):

    p = 0
    if request.POST:
        if 'Accept' in request.POST:
            for req in OtherRequest.objects.filter(other__user=request.user, approval_status=0):
                p = 1
                stud = str(req.student.rollnumber)
                if request.POST.getlist(stud)[0] == 'YES':

                    req.approval_status = 2
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION"
                    mess="Your application for " + str(req.other.user.username) + " has been APPROVED! "
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark
                    send_emailll(useremail,mess)
        elif 'Reject' in request.POST:
            for req in OtherRequest.objects.filter(other__user=request.user, approval_status=0):

                p = 1
                stud = str(req.student.rollnumber)
                if request.POST.getlist(stud)[0] == 'YES':

                    req.approval_status = 3
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION"
                    mess="Your application for " + str(req.other.user.username) + " has been REJECTED! "
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark
                    mess+="\nKindly pay your dues and apply again!"
                    send_emailll(useremail,mess)
        else:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return HttpResponseRedirect(reverse("otherIndex"))

            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("otherIndex"))

            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            lines.pop()
            c = 0
            f = 0
            for line in lines:
                fields = line.split(",")
                if(len(fields) >= 2):
                    if(fields[0].isdigit()):
                        c = c + 1
                        if 'AcceptCSV' in request.POST:
                            for req in OtherRequest.objects.filter(other__user=request.user,student__rollnumber=fields[0],approval_status=0):
                                req.approval_status = 2
                                req.remark = fields[1]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.other.user.username) + " has been APPROVED! "
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                send_emailll(useremail,mess)
                        if 'RejectCSV' in request.POST:
                            for req in OtherRequest.objects.filter(other__user=request.user,student__rollnumber=fields[0],approval_status=0):
                                req.approval_status = 3
                                req.remark = fields[1]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.other.user.username) + " has been REJECTED!"
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                mess+="\nKindly pay your dues and apply again!"
                                send_emailll(useremail,mess)
                else:
                    messages.error(request,'Incorrect File Format!\nEvery Row should have atleast two entries,\nFirst entry being rollnumber and the second being the remark')
                    f = 1
                    break
            if c == 0 and f == 0:
                messages.error(request,'Incorrect File Format!\nEvery Row should have atleast two entries,\nFirst entry being rollnumber and the second being the remark')
        return HttpResponseRedirect(reverse('mainPage'))


    if request.user.is_authenticated:

        dictTemp = OtherUserInfo.objects.filter(user=request.user)
        if len(dictTemp) == 0:
            return HttpResponseRedirect(reverse('mainPage'))

        requests = OtherRequest.objects.filter(other__user=request.user, approval_status=0)
        if requests:
            p = 1
        return render(request, 'main_app/other_main_page.html', {'requests': requests, 'p' : p });

    return HttpResponseRedirect(reverse('mainPage'))


def hodIndex(request):

    if request.POST:
        dicts = HODUserInfo.objects.get(user=request.user)
        if 'AcceptLAB' in request.POST:
            for req in LabRequests.objects.filter(lab__department=dicts.department, approval_status=1):
                stud = str(req.student.rollnumber)+str(req.lab.user.username)
                if request.POST.getlist(stud)[0] == 'YES':
                    req.approval_status = 2
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION"
                    mess="Your application for " + str(req.lab.user.username) + " has been APPROVED!"
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark
                    send_emailll(useremail,mess)

        elif 'RejectLAB' in request.POST:
            for req in LabRequests.objects.filter(lab__department=dicts.department, approval_status=1):
                stud = str(req.student.rollnumber)+str(req.lab.user.username)
                if request.POST.getlist(stud)[0] == 'YES':
                    req.approval_status = 3
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION"
                    mess="Your application for " + str(req.lab.user.username) + " has been REJECTED!"
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark
                    mess+="\nKindly pay your dues and apply again!"
                    send_emailll(useremail,mess)
        elif 'AcceptBTP' in request.POST:
            for req in BTPRequest.objects.filter(btp__department=dicts.department, approval_status=1):
                stud = str(req.student.rollnumber)+str(req.btp.user.username)
                if request.POST.getlist(stud)[0] == 'YES':
                    req.approval_status = 2
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION" 
                    mess="Your application for " + str(req.btp.user.username) + " has been APPROVED!"
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark            
                    send_emailll(useremail,mess)
            for req in BTPRequest.objects.filter(hod__user=request.user, approval_status=1):
                stud = str(req.student.rollnumber)+str(req.hod.user.username)
                if request.POST.getlist(stud)[0] == 'YES':
                    req.approval_status = 2
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION"
                    mess="Your application for " + str(req.hod.user.username) + " has been APPROVED!"
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark
                    send_emailll(useremail,mess)
        elif 'RejectBTP' in request.POST:
            for req in BTPRequest.objects.filter(btp__department=dicts.department, approval_status=1):
                stud = str(req.student.rollnumber)+str(req.btp.user.username)
                if request.POST.getlist(stud)[0] == 'YES':
                    req.approval_status = 3
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION"
                    mess="Your application for " + str(req.btp.user.username) + " has been REJECTED!"
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark
                    mess+="\nKindly pay your dues and apply again!"
                    send_emailll(useremail,mess) 
            for req in BTPRequest.objects.filter(hod__user=request.user, approval_status=1):
                stud = str(req.student.rollnumber)+str(req.hod.user.username)
                if request.POST.getlist(stud)[0] == 'YES':
                    req.approval_status = 3
                    req.remark = request.POST.getlist(stud)[1]
                    req.save()
                    useremail=req.student.user.email
                    subject="NO DUES APPLICATION"
                    mess="Your application for " + str(req.hod.user.username) + " has been REJECTED!"
                    if(req.remark):
                        mess+=" with the REMARK :\n "+req.remark
                    mess+="\nKindly pay your dues and apply again!"
                    send_emailll(useremail,mess)
        else:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return HttpResponseRedirect(reverse("hodIndex"))
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return HttpResponseRedirect(reverse("hodIndex"))
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            lines.pop()
            c = 0
            f = 0
            for line in lines:
                fields = line.split(",")
                if(len(fields) >= 3):
                    if(fields[0].isdigit()):
                        c = c + 1
                        if 'AcceptCSVLAB' in request.POST:
                            for req in LabRequests.objects.filter(lab__department=dicts.department,student__rollnumber=fields[0],lab__user__username=fields[1] , approval_status=1):
                                req.approval_status = 2
                                req.remark = fields[2]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.lab.user.username) + "has been APPROVED!"
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                
                                send_emailll(useremail,mess)
                        if 'RejectCSVLAB' in request.POST:
                            for req in LabRequests.objects.filter(lab__department=dicts.department,student__rollnumber=fields[0],lab__user__username=fields[1] , approval_status=1):
                                req.approval_status = 3
                                req.remark = fields[2]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.lab.user.username) + "has been REJECTED!"
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                mess+="\nKindly pay your dues and apply again!"
                                send_emailll(useremail,mess)
                        if 'AcceptCSVBTP' in request.POST:
                            for req in BTPRequest.objects.filter(btp__department=dicts.department,student__rollnumber=fields[0],btp__user__username=fields[1] , approval_status=1):
                                req.approval_status = 2
                                req.remark = fields[2]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.btp.user.username) + "has been APPROVED!"
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                mess+="\nKindly pay your dues and apply again!"
                                send_emailll(useremail,mess)
                            for req in BTPRequest.objects.filter(student__rollnumber=fields[0],hod__user=request.user , approval_status=1):
                                req.approval_status = 2
                                req.remark = fields[2]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.hod.user.username) + "has been APPROVED!"
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                mess+="\nKindly pay your dues and apply again!"
                                send_emailll(useremail,mess)
                        if 'RejectCSVBTP' in request.POST:
                            for req in BTPRequest.objects.filter(btp__department=dicts.department,student__rollnumber=fields[0],btp__user__username=fields[1] , approval_status=1):
                                req.approval_status = 3
                                req.remark = fields[2]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.btp.user.username) + "has been REJECTED!"
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                mess+="\nKindly pay your dues and apply again!"
                                send_emailll(useremail,mess)
                            for req in BTPRequest.objects.filter(student__rollnumber=fields[0],hod__user=request.user , approval_status=1):
                                req.approval_status = 3
                                req.remark = fields[2]
                                req.save()
                                useremail=req.student.user.email
                                subject="NO DUES APPLICATION"
                                mess="Your application for " + str(req.hod.user.username) + "has been REJECTED!"
                                if(req.remark):
                                    mess+=" with the REMARK :\n "+req.remark
                                mess+="\nKindly pay your dues and apply again!"
                                send_emailll(useremail,mess)
                else:
                    messages.error(request,'Incorrect File Format!\nEvery Row should have atleast three entries,\nFirst entry being rollnumber, second being  lab/btp and the third being the remark')
                    f = 1
                    break
            if c == 0 and f == 0:
                messages.error(request,'Incorrect File Format!\nEvery Row should have atleast three entries,\nFirst entry being rollnumber, second being  lab/btp and the third being the remark')

        return HttpResponseRedirect(reverse('mainPage'))


    if request.user.is_authenticated:
        dicts = HODUserInfo.objects.filter(user=request.user)
        for dict in dicts:
            department = dict.department
            requests = LabRequests.objects.filter(lab__department=department, approval_status=1)
            requests2=BTPRequest.objects.filter(btp__department=department, approval_status=1)
            requests3=BTPRequest.objects.filter(hod__user=request.user, approval_status=1)
            requests2 = requests2.union(requests3)
            return render(request, 'main_app/hod_main_page.html', {'requests': requests, 'requests2':requests2 });
    return HttpResponseRedirect(reverse('mainPage'))



def studentBTP(request):
    if request.user.is_authenticated:
        btpRequests = BTPRequest.objects.filter(student__user=request.user)
        return render(request, 'main_app/student_btp_page.html', {'btpRequests': btpRequests})
    return render(request, 'main_app/student_btp_page.html')

def studentLab(request):
    if request.user.is_authenticated:
        labRequests = LabRequests.objects.filter(student__user=request.user)
        return render(request, 'main_app/student_lab_page.html', {'labRequests': labRequests})
    return render(request, 'main_app/student_lab_page.html')

def studentOther(request):
    if request.user.is_authenticated:
        otherRequests = OtherRequest.objects.filter(student__user=request.user)
        return render(request, 'main_app/student_other_page.html', {'otherRequests': otherRequests})
    return render(request, 'main_app/student_other_page.html')

def registerStudent(request):
    registered = False
    if request.method == "POST":
        user_form = StudentUserForm(data=request.POST)
        info_form = StudentsInfoForm(data=request.POST)
        if user_form.is_valid() and info_form.is_valid():
            user = user_form.save();
            user.set_password(user.password)
            user.save()
            profile = info_form.save(commit=False)
            profile.user = user;
            profile.save()
            registered = True
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('studentIndex'))

                else:
                    return HttpResponse('ACCOUNT NOT ACTIVE')
            else:
                return HttpResponse("invalid login details supplied")
    else:
        user_form=StudentUserForm()
        info_form=StudentsInfoForm()
    return render(request, 'main_app/register_page.html', {'user_form': user_form, 'info_form': info_form, 'registered': registered, 'registerFlag': 0})


def registerLab(request):
    registered = False
    if request.method == "POST":

        print('post', request.POST)

        user_form = LabUserForm(data=request.POST)
        info_form = LabInfoForm(data=request.POST)
        if user_form.is_valid() and info_form.is_valid():
            user = user_form.save();
            user.set_password(user.password)
            user.save()

            profile = info_form.save(commit=False)
            profile.user = user;

            profile.save()

            if '1' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="CSE"))

            if '2' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="MnC"))

            if '3' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="ECE"))

            if '4' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="EEE"))

            if '5' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="CL"))

            if '6' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="CE"))

            if '7' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="CST"))

            if '8' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="ME"))

            if '9' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="BT"))

            if '10' in request.POST.getlist('department'):
                profile.department.add(Department.objects.get(name="EP"))


            registered = True
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('labIndex'))
                else:
                    return HttpResponse('ACCOUNT NOT ACTIVE')
            else:
                return HttpResponse("invalid login details supplied")
    else:
        user_form=LabUserForm()
        info_form=LabInfoForm()
    return render(request, 'main_app/register_page.html', {'user_form': user_form, 'info_form': info_form, 'registered': registered, 'registerFlag': 1})

def registerHOD(request):
    registered = False
    if request.method == "POST":
        user_form = HODUserForm(data=request.POST)
        info_form = HODInfoForm(data=request.POST)
        if user_form.is_valid() and info_form.is_valid():
            user = user_form.save();
            user.set_password(user.password)
            user.save()
            profile = info_form.save(commit=False)
            profile.user = user;
            profile.save()
            registered = True
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('hodIndex'))
                else:
                    return HttpResponse('ACCOUNT NOT ACTIVE')
            else:
                return HttpResponse("invalid login details supplied")
    else:
        user_form=HODUserForm()
        info_form=HODInfoForm()
    return render(request, 'main_app/register_page.html', {'user_form': user_form, 'info_form': info_form, 'registered': registered, 'registerFlag': 4})



def registerOther(request):
    registered = False
    if request.method == "POST":
        user_form = OtherUserForm(data=request.POST)
        info_form = OtherInfoForm(data=request.POST)
        if user_form.is_valid() and info_form.is_valid():
            user = user_form.save();
            user.set_password(user.password)
            user.save()
            profile = info_form.save(commit=False)
            profile.user = user;
            profile.save()
            registered = True
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('otherIndex'))
                else:
                    return HttpResponse('ACCOUNT NOT ACTIVE')
            else:
                return HttpResponse("invalid login details supplied")
    else:
        user_form=OtherUserForm()
        info_form=OtherInfoForm()

    return render(request, 'main_app/register_page.html', {'user_form': user_form, 'info_form': info_form, 'registered': registered, 'registerFlag': 2})

def registerBTP(request):
    registered = False
    if request.method == "POST":
        user_form = BTPUserForm(data=request.POST)
        info_form = BTPInfoForm(data=request.POST)
        if user_form.is_valid() and info_form.is_valid():
            user = user_form.save();
            user.set_password(user.password)
            user.save()
            profile = info_form.save(commit=False)
            profile.user = user;
            profile.save()
            registered = True
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('btpIndex'))
                else:
                    return HttpResponse('ACCOUNT NOT ACTIVE')
            else:
                return HttpResponse("invalid login details supplied")
    else:
        user_form=BTPUserForm()
        info_form=BTPInfoForm()
    return render(request, 'main_app/register_page.html', {'user_form': user_form, 'info_form': info_form, 'registered': registered, 'registerFlag': 3})




def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                dict1 = StudentUserInfo.objects.filter(user=request.user)
                if len(dict1)>0:
                    return HttpResponseRedirect(reverse('studentIndex'))
                else:
                    dict2 = LabUserInfo.objects.filter(user=request.user)
                    if len(dict2)>0:
                        return HttpResponseRedirect(reverse('labIndex'));
                    else:
                        dict3 = OtherUserInfo.objects.filter(user=request.user)
                        if len(dict3)>0:
                            return HttpResponseRedirect(reverse('otherIndex'))
                        else:
                            dict4 = BTPUserInfo.objects.filter(user=request.user)
                            if len(dict4)>0:
                                return HttpResponseRedirect(reverse('btpIndex'))
                            else:
                                dict5 = HODUserInfo.objects.filter(user=request.user)
                                if len(dict5)>0:
                                    return HttpResponseRedirect(reverse('hodIndex'))
                                else:
                                    dict6 = HeavenUserInfo.objects.filter(user=request.user)
                                    if len(dict6)>0:
                                        return HttpResponseRedirect(reverse('heavenIndex'))
                                    else:
                                        return HttpResponse("unable to log in")
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            return HttpResponse("invalid login details supplied")
    else:
        return render(request, 'main_app/base.html', {})

def change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('studentIndex'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main_app/change_password.html', {
        'form': form
    })

def apply_page(request):

    context = initialize_context(request)

    student = StudentUserInfo.objects.get(user__email=context['user']['email'])
    try:
        othreqs = OtherRequest.objects.filter(student=student)
    except OtherRequest.DoesNotExist:
        othreqs = None
    try:
        labreqs = LabRequests.objects.filter(student=student)
    except LabRequests.DoesNotExist:
        labreqs = None
    try:
        btpreq = BTPRequest.objects.get(student=student)
    except BTPRequest.DoesNotExist:
        btpreq = None
    try:
        btps = BTPUserInfo.objects.filter(approval_status=1)
        btps2 = HODUserInfo.objects.filter(isBTP=True)
        btps = btps.union(btps2)
    except BTPUserInfo.DoesNotExist or HODUserInfo.DoesNotExist:
        btps = None
    try:
        labs = LabUserInfo.objects.filter(department__in=[student.department], prog=student.prog, approval_status=1)
    except LabUserInfo.DoesNotExist:
        labs = None
    l = 0
    h = 0
    b = 0
    op = 0
    k = 0
    g = 0
    arr = []
    if labs:
        for labx in labs:
            if labreqs:
                try:
                    labrc = labreqs.get(lab=labx)
                except:
                    labrc = None
                if labrc:
                    if labrc.approval_status in (0,1,2):
                        arr.append(1)
                    else:
                        arr.append(0)
                        op = 1
                else:
                    arr.append(0)
                    op = 1
            else:

                arr.append(0)
                op = 1

    if btpreq:
        if btpreq.approval_status in (0,1,2):
            b = 1

    for req in othreqs:
        if req.other.user.username == 'LibraryCCC' and req.approval_status in (0,1,2) :
            l = 1
        if req.other.user.username == 'Gymkhana' and req.approval_status in (0,1,2) :
            g = 1
        if req.other.user.username == 'LOHIT'  and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'SIANG' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'DIHING' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'MANAS' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'KAPILI' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'UMIAM' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'BRAHMAPUTRA' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'BARAK' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'KAMENG' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'MSH' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'DHANSIRI' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'SUBANSIRI' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'DIBANG' and req.approval_status in (0,1,2) :
            h = 1
        if req.other.user.username == 'DISANG' and req.approval_status in (0,1,2) :
            h = 1

    if l == 1 and h == 1 and b == 1 and op == 0 and g == 1 :
        k = 1

    context['student'] = student;
    context['btps'] = btps;
    context['labs'] = labs;
    context['labreqs'] = labreqs
    context['othreqs'] = othreqs
    context['btpreq'] = btpreq
    context['l'] = l
    context['h'] = h
    context['b'] = b
    context['op'] = op
    context['k'] = k
    context['arr'] = arr
    context['g'] = g

    return render(request, 'main_app/apply.html', context)




def hod_btp_approval_page(request):

    if request.POST:
        dicts = HODUserInfo.objects.get(user=request.user)
        if 'AcceptBTPAC' in request.POST:
            for req in BTPUserInfo.objects.filter(department=dicts.department, approval_status=0):
                stud = str(req.user.username)
                if request.POST.get(stud) == 'YES':
                    req.approval_status = 1
                    req.save()
            return HttpResponseRedirect(reverse('btpAccountRequests'))

        elif 'RejectBTPAC' in request.POST:
            for req in BTPUserInfo.objects.filter(department=dicts.department, approval_status=0):
                stud = str(req.user.username)
                if request.POST.get(stud) == 'YES':
                    req.user.delete()
                    req.delete()

            return HttpResponseRedirect(reverse('btpAccountRequests'))

    if request.user.is_authenticated:
        dicts = HODUserInfo.objects.filter(user=request.user)
        for dict in dicts:
            department = dict.department
            requests = BTPUserInfo.objects.filter(department=department, approval_status=0)
            return render(request, 'main_app/hod_btp_approval_page.html', {'requests': requests });
    return HttpResponseRedirect(reverse('mainPage'))

def hod_lab_approval_page(request):

    if request.POST:

        dicts = HODUserInfo.objects.get(user=request.user)
        if 'AcceptLABAC' in request.POST:
            for req in LabUserInfo.objects.filter(department=dicts.department, approval_status=0):
                stud = str(req.user.username)
                if request.POST.get(stud) == 'YES':
                    req.approval_status = 1
                    req.save()
            return HttpResponseRedirect(reverse('labAccountRequests'))
        elif 'RejectLABAC' in request.POST:
            for req in LabUserInfo.objects.filter(department=dicts.department, approval_status=0):
                stud = str(req.user.username)
                if request.POST.get(stud) == 'YES':
                    req.user.delete()
                    req.delete()
            return HttpResponseRedirect(reverse('labAccountRequests'))

    if request.user.is_authenticated:
        dicts = HODUserInfo.objects.filter(user=request.user)
        for dict in dicts:
            department = dict.department
            requests = LabUserInfo.objects.filter(department__in=[department], approval_status=0)
            return render(request, 'main_app/hod_lab_approval_page.html', {'requests': requests });
    return HttpResponseRedirect(reverse('labAccountRequests'))










# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 465

# EMIL_USE_TLS = False
# EMAIL_USE_SSL = True