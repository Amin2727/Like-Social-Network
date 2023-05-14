from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# این قسمت مربوط میشه به جلسه ی ۴۵ که بحث سیگنالها بود میگه اگه سیگنالی اومد وصل کن به فانکشن
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
	if kwargs['created']:
		Profile.objects.create(user=kwargs['instance'])

# ایمپورت پست سیو فراموش نشه
# post_save.connect(receiver=create_profile, sender=User)
# مایک سیگنالی ایجاد کردیم که حواسش به مدل یوزر هست که اگر سیو شد بعدش اون سیگنال رو ارسال میکنیم به فانکشن بالا و داخل فانکشن چک میکنیم که اگر کریتد ترو بود یعنی اگر چیزی با موفقیت سیو شده بود خود اون اینستس که سیو شده بود رو میگیریم و یه کار خاصی رو انجام میدیم روش
# در داخل اپز دات پای میای داخل متد ردی سیگنالز رو ایمپورت میکنیم که جنگو شعورش برسه بشناسه سیگنالها رو