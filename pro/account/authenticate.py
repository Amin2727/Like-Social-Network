from django.contrib.auth.models import User

# این یوزرنیم و پسورد همون یوزرنیم و پسوردی هستش که ما موقع اوتنتیکیت کردن بهش ارسال میکردیم در لاگین ویو قسمت متد پست
class EmailBackend():
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        # جنگو از توی مدل یوزر یه اکسپشن به نام داز نات اگزیست رو میاره
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
         # جنگو از توی مدل یوزر یه اکسپشن به نام داز نات اگزیست رو میاره
        except User.DoesNotExist:
            return None
        
# باید کلاس بالا رو بدیم به آپشن اوتینتیکیشن بک اند وگرنه جنگو از این خبر نداره و اجرا نمیکنه برنامه رو... در ستینگز خط آخر مشخص کردم