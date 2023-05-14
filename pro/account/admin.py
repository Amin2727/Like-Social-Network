from django.contrib import admin
from .models import Relation, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# مربوط به جلسه ی ۴۳ که میاد طبق مدل پروفایل، پروفایل رو اضافه میکنه به ته مدل یوزر در ادمین پنل جنگومون
class ProfileInline(admin.StackedInline):
    model = Profile

    # خط زیر رو بنویسیم دیگه کسی نمیتونه از توی ادمین پنل پروفایل کسی دیگه رو پاک کنه در واقع تیک دیلیتی که وجود داشت کنار پروفایل حذف میشه
    can_delete = False

class ExtendedUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)



admin.site.register(Relation)
