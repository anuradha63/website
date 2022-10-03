from django.contrib import admin
from main_app.models import Department, StudentUserInfo, HODUserInfo, LabUserInfo, BTPUserInfo, OtherUserInfo, LabRequests, BTPRequest, OtherRequest, HeavenUserInfo, Prog
# Register your models here.

admin.site.register(Department)
admin.site.register(StudentUserInfo)
admin.site.register(HODUserInfo)
admin.site.register(LabUserInfo)
admin.site.register(BTPUserInfo)
admin.site.register(OtherUserInfo)
admin.site.register(LabRequests)
admin.site.register(BTPRequest)
admin.site.register(OtherRequest)
admin.site.register(HeavenUserInfo)
admin.site.register(Prog)
