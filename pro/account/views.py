from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation

class UserRegisterView(View):
	# چون دوخط زیر زیاد در برنامه استفاده شد در کلاس وریبل ذخیره شون کردیم و از وریبلشون استفاده کردیم به جای خودشون
	form_class = UserRegistrationForm
	template_name = 'account/register.html'

	# متد دیسپچ قبل از همه ی خطوط پایین اجرا میشه در اینجا اگر کاربر لاگین کرده باشه و بخواد به صورت دستی بره قسمت رجیستر ثبت نام هدایت میشه به هوم
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home:home')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request):
		form = UserRegistrationForm()
		return render(request, self.template_name, {'form':form})
	
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			User.objects.create_user(cd['username'], cd['email'], cd['password1'])
			messages.success(request, 'you registered successfully', 'success')
			return redirect('home:home')
		return render(request, self.template_name, {'form':form})
	

# برای جلسه ی ۱۱ بود که لاگین کردن رو نوشتیم برنامه شو + فرمهاش + یوآرالش
class UserLoginView(View):
	form_class = UserLoginForm
	template_name = 'account/login.html'

	# برای جلسه ی ۳۴ دوره هستش که میاد متد نکست رو از طریق متد ست آپ تعیین میکنه که اگه کاربر از طریق پست رفت روی اسم خودش و بعد هدایت شد به صفحه ی لاگین و لاگین کرد دوباره ریدایرکت بشه به صفحه ی پروفایل خودش
	def setup(self, request, *args, **kwargs):
		self.next = request.GET.get('next')
		return super().setup(request, *args, **kwargs)


	# این متد متدی هست که قبل از بقیه اجرا خواهد شد در اینجا اگر لاگین کرده باشه کاربر و بخواد به صورت دستی بره قسمت لاگین هدایت میشه به صفحه ی هوم
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home:home')
		return super().dispatch(request, *args, **kwargs)
	

	def get(self, request):
		form = self.form_class
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'success')
				# مربوط به جلسه ۳۴ ادامه ش هست میگه اگه داخل نکست چیزی بود ریدایرکتش کن به 
				if self.next:
					return redirect(self.next)
				return redirect('home:home')
			messages.error(request, 'username or password is wrong', 'warning')
		return render(request, self.template_name, {'form':form})
	

# در جلسه ی ۱۲ نوشته شد
# در جلسه ی ۱۳ که دیسپچها گفته شد
# در جلسه ی ۱۴ اومدیم برای اینکه کاربری که لاگین کرده نره قسمت لاگ اوت، در ستینگز لاگین یوآرالی نوشتیم که هدایتش کنه به صفحه ی لاگین
class UserLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'You logged out successfully.', 'success')
		return redirect('home:home')
	

# مربوط به جلسه ی ۱۶ ساخت پروفایل کاربری
class UserProfileView(LoginRequiredMixin, View):
	def get(self, request, user_id):
		# مربوط به جلسه ۳۳ فالو و آنفالو کردن
		is_following = False
		user = get_object_or_404(User, pk=user_id)
		# posts = Post.objects.filter(user=user) در جلسه ی ۳۲ بنا به ایجاد ریلیتد نیم اومدیم کد پایینو به جای این نوشتیم
		posts = user.posts.all()
		# مربوط به جلسه ی ۳۳ هستش که فالو و آنفالو کردن رو اینجا نوشتیم کوءری هاشو
		relation = Relation.objects.filter(from_user=request.user, to_user=user)
		if relation.exists():
			is_following = True

		context =  {
			'user':user, 
	      	'posts':posts, 
			'is_following':is_following
			}
		
		return render(request, 'account/profile.html', context)
	
	
# این کلاس و سه تای بعدش برای فراموشی رمز عبور هست که تنظیماتشو تو ستینگز تو بخش گوگل اکانت گذاشتیم
class UserPasswordResetView(auth_views.PasswordResetView):
	template_name = 'account/password_reset_form.html'
	success_url = reverse_lazy('account:password_reset_done')
	email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
	template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
	template_name = 'account/password_reset_confirm.html'
	success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
	template_name = 'account/password_reset_complete.html'


# مربوط به جلسه ی ۳۳ هستش که میایم اول مدل و بعد یوآرال و بعد ویوی فالو و آنفالو رو میسازیم
class UserFollowView(LoginRequiredMixin, View):
	def get(self, request, user_id):
		user = User.objects.get(id=user_id)
		# اگزیستز فقط روی فیلتر کار میکنه با گت و اینا کار نمیکنه
		relation = Relation.objects.filter(from_user = request.user, to_user = user)
		if relation.exists():
			messages.error(request, 'You are already following this user!', 'danger')
		else:
			relation = Relation.objects.create(from_user = request.user, to_user = user)
			relation.save()
			messages.success(request, 'You followed this user.', 'success')
		return redirect('account:user_profile', user.id)	



class UserUnfollowView(LoginRequiredMixin, View):
	def get(self, request, user_id):
		user = User.objects.get(id=user_id)
		relation = Relation.objects.filter(from_user=request.user, to_user=user)
		if relation.exists():
			relation.delete()
			messages.success(request, 'you unfollowed this user', 'success')
		else:
			messages.error(request, 'you are not following this user', 'danger')
		return redirect('account:user_profile', user.id)



# مربوط به جلسه ی ۴۴ دوره ست که میایم ویوی ادیت یوزر رو میسازیم که بتونیم پروفایل کاربر رو تغییر بدیم
class EditProfileView(LoginRequiredMixin, View):
	form_class = EditProfileForm

	def get(self, request):
		form = self.form_class(instance=request.user.profile, initial={'email':request.user.email, 'first_name':request.user.first_name, 'last_name':request.user.last_name})
		return render(request, 'account/edit_profile.html', {'form':form})
	
	def post(self, request):
		form = self.form_class(request.POST, instance=request.user.profile)
		if form.is_valid():
			form.save()
			request.user.email = form.cleaned_data['email']
			request.user.first_name = form.cleaned_data['first_name']
			request.user.last_name = form.cleaned_data['last_name']
			request.user.save()
			messages.success(request, 'Profile edited successfully!', 'success')
		return redirect('account:user_profile', request.user.id)