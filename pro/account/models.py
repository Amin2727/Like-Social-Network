from django.db import models
from django.contrib.auth.models import User

# Follow and Unfollow Model

class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'


# جلسه ی ۴۳ مربوط به ساخت مدل یوزر با روش اکستند که میایم تو پرفایل ادمین پنل یه سری فیلد هایی که خودمون میخوایمو اضافه میکنیم بهش
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user} - {self.age} - {self.city}'