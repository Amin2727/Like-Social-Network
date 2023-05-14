from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile

class UserRegistrationForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Like Amin'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Name@gmail.com'}))
	password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

	# در جلسه ی ۹ دو تا کار انجام شد: یک. اول اومدیم کاری کردیم که با ایمیلی که قبلا کسی ازش استفاده کرده کاربری که میخواد ثبت نام کنه نتونه ازش استفاده کنه و به ارور بخوره
	# متد کلین میاد توو پایتون و ولیدیت و ران ولیدیتورز که فیلد های اعتبارسنجی هستند رو همزمان اجرا میکنه
	# clean_<filed_name>
	def clean_email(self):
		email = self.cleaned_data['email']
		user = User.objects.filter(email=email).exists()
		if user:
			raise ValidationError('This email already exists!')
		return email

	# دو. به جای یک پسورد دوتا پسورد گذاشتیم که دومیش تایید پسورد هستش و در ویو هم باید به جای پسورد خالی، پسورد ۱ رو بگیره از کلیند دیتا
	def clean(self):
		cd = super().clean()
		p1 = cd.get('password1')
		p2 = cd.get('password2')

		if p1 and p2 and p1 != p2:
			raise ValidationError('password must match...')


class UserLoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


# مربوط به جلسه ی ۴۴ دوره ست که میاد فرم ادیت پروفایل رو میداریم با استفاده از مدل فرمها
class EditProfileForm(forms.ModelForm):
	# این فیلدها رو اضافه کردیم به لیست ادیتهامون چون توی مدل پروفایل نبود جدا اضافه ش کردیم
	email = forms.EmailField()
	first_name = forms.CharField()
	last_name = forms.CharField()

	class Meta:
		model = Profile
		fields = ('age', 'bio', 'city')