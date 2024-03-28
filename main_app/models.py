from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.
class Prog(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length = 264, unique=True)

    def __str__(self):
        return self.name

class HeavenUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class StudentUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollnumber = models.IntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    prog = models.ForeignKey(Prog,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return  str(self.rollnumber)  + "--" + self.user.username

class HODUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    isBTP = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + "--" + str(self.department.name)

class LabUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ManyToManyField('Department')
    approval_status=models.IntegerField(default=0)
    prog = models.ForeignKey(Prog,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.user.username

class BTPUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    approval_status=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username + "--" + str(self.department.name)

class OtherUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class LabRequests(models.Model):
    lab = models.ForeignKey(LabUserInfo, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUserInfo, on_delete=models.CASCADE)

    remark = models.CharField(max_length=300,null=True);
    date_sent = models.DateField()

    #0-waiting, 1-waiting for hod, 2-approved, 3-rejected, 4-not sent yet

    approval_status = models.IntegerField()

    def __str__(self):
        return str(self.student.rollnumber)+"--"+self.lab.user.username

class BTPRequest(models.Model):
    btp = models.ForeignKey(BTPUserInfo, on_delete=models.CASCADE, null=True)
    hod = models.ForeignKey(HODUserInfo, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(StudentUserInfo, on_delete=models.CASCADE)

    remark = models.CharField(max_length=300,null=True);
    date_sent = models.DateField()

    #0-waiting, 1-waiting for hod, 2-approved, 3-rejected, 4-not sent yet

    approval_status = models.IntegerField()

    def __str__(self):
        if self.btp:
            return str(self.student.rollnumber)+"--"+self.btp.user.username
        else:
            return str(self.student.rollnumber)+"--"+self.hod.user.username

class OtherRequest(models.Model):
    other = models.ForeignKey(OtherUserInfo, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUserInfo, on_delete=models.CASCADE)

    remark = models.CharField(max_length=300,null=True);
    date_sent = models.DateField()

    #0-waiting, 1-approved, 3-rejected, 4-not sent yet

    approval_status = models.IntegerField()

    def __str__(self):
        return str(self.student.rollnumber)+"--"+self.other.user.username
