from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# مربوط به جلسه ی ۱۷ ایجاد مدل پست هست، اسلاگ رشته ای هستش که برای خوانایی یوآرال استفاده میشود
class Post(models.Model):
    # ریلیتد نیم میاد کمک میکنه که ما بفهمیم یو یوزر چند تا پست داره در اکانت قسمت یوزرپروفایل ویو خط دوم متد گت به جای کدش از همین ریلیتد نیم استفاده کردیم
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.slug} - {self.created}'
    
    # این مربوط میشه به جلسه ی ۳۱ که میاد بر اساس پستهای ایجاد شده نزولی سفارش سازی میکنه
    class Meta:
         ordering = ['-created']
    
    # برای جلسه ۱۸ هستش که اینو نوشتیم برای مرتب شدن یوآرال پست دیتیلها
    def get_absolute_url(self):
         return reverse('home:post_detail', args=(self.id, self.slug))
    
	# جلسه ی ۴۰ اومدیم این رو نوشتیم که در ویو نشون بدیم چند بار لایک شده پست کاربر
    def like_count(self):
         return self.pvotes.count()
    
    # مربوط به جلسه ی ۴۰ که میاد میبینه اگه کسی پستی رو لایک کرده بود بیاد گزینه لایک رو دیسیبل کنه
    def user_can_like(self, user):
         user_like = user.uvotes.filter(post=self)
         if user_like.exists():
              return True
         return False
         
    
# مربوط به جلسه ی ۳۵هست که مدل کامنت گذاشتن رو نوشتیم
# نکته: اگر مدل کامنت بالای مدل پست بود باید پست رو داخل کوتیشن بذاریم ولی الان چون مدل کامنت پایین مدل پست هست خود پست رو مینویسیم و ایرادی نداره
class Comment(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
     body = models.TextField(max_length=400)
     reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
     is_reply = models.BooleanField(default=False)
     created = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f'{self.user} - {self.body[:30]}'



# مربوط به جلسه ۴۰ لایک کردن
class Vote(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvotes')

     def __str__(self):
          return f'{self.user} votes {self.post.slug}'