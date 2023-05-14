from django.shortcuts import (
    render, 
    redirect, 
    get_object_or_404,
    )
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from .models import (
    Post, 
    Comment, 
    Vote,
    )
from .forms import (
    PostCreateUpdateForm, 
    CommentCreateForm, 
    CommentReplyForm, 
    PostSearchForm,
    )
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    # مربوط به جلسه ی ۴۱ هست که کلاس سرچ فرم رو دادیم به این ویو
    form_class = PostSearchForm
    def get(self, request):
        posts = Post.objects.all()
        # مربوط به جلسه ی ۴۰ که برنامه ی سرچ کردن رو نوشتیم دو خط زیر اینه
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        context = {
            'posts':posts,
            'form':self.form_class
            }
        return render(request, 'home/home.html', context)
    

class PostDetailView(View):
    # مربوط به جلسه ی ۳۷ برای کامنت گذاشتنه به رندر اضافه ش کردیم و در دیتیل شرطی نوشتیم که فقط کسایی که لاگین کردن بتونن کامنت بذارن
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    # مربوط به جلسه ی ۳۷ هست
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, post_id, post_slug):
        # post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        # مربوط به جلسه ی ۳۶ هست که میاد از پستها کامنتهاشونو میخونه از مدل پست میریم ریلیتدنیم پست مدل کامنت رو همه شو میخونیم
        comments = self.post_instance.pcomments.filter(is_reply=False)
        # مربوط به جلسه ی ۴۰ هست که میاد از متدی که توی مدل نوشتیم استفاده میکنه که بگه اگه یوزر لایک کرده بود گزینه لایک رو دیسبیل بکنه توی تمپلیت تا دوخط بعد کن لایک که شرطه
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        context = {
            'post':self.post_instance, 
            'comments':comments, 
            'form':self.form_class, 
            'reply_form':self.form_class_reply,
            'can_like':can_like
            }
        return render(request, 'home/detail.html', context)
    
    # مربوط به جلسه ی ۳۷ هستش که میاد لاگین ریکوآیرد رو از طریق متد دیکوریتور میده به متدمون
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
           new_comment = form.save(commit=False)
           new_comment.user = request.user
           new_comment.post = self.post_instance
           new_comment.save()
           messages.success(request, 'Your comment submitted successfully.', 'success')
           return redirect('home:post_detail', self.post_instance.id, self.post_instance.slug)

# جلسه۲۱ ساخت دیلیت ویو برای حذف پست
class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post ,pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'You deleted post seccessfully!', 'success')
        else:
            messages.error(request, 'You cant delete this post', 'danger')
        return redirect('home:home')

# مربوط به جلسه ۲۲ ساخت ویوی آپدیت پستها
# در جلسه ۲۴ اومدیم کریت رو قبل از آپدیت به اسم کلاس وریبل کلاس پست آپدیت اضافه کردم چون تو فرمها اسمشو تغییر دادم
class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    # چون ما بررسی اینکه کاربری که درخواست آپدیت زده اگه آیدیش برابر نبود با آیدی پست بیاد پیغام ارور نشونش بده رو تکرار کرده بودیم در متد گت و پست اومدیم در متد دیسپچ این بررسی رو قرار دادیم که کدامون شلوغ نشه... برای جلسه ۲۲ هستش
    # متد ستاپ اطلاعاتی که قراره داخل متدها استفاده بشن رو داخل خودش ذخیره میکنه که یه بار بریم وصل شیم به دیتابیس
    # متد ستاپ قبل از دیسپچ اجرا خواهد شد
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request,*args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "You can't update this post!", 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    # جای آرگز و کیوارگز پست آیدی بود که از طریق یوآرال میومد ولی اگه ننویسیمش ارور میگیریم پس بنا به تمیزی کد باید به جاش از آرگز و گیوارگز استفاده کنیم
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form':form, 'post':post})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, "You updated this post.", 'success')
            return redirect('home:post_detail', post.id, post.slug)
        

# جلسه ی ۲۴ هست که مربوط به ساخت پست هست
class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'home/create.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'You created a new post.', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)
        

# مربوط به جلسه ۳۹ ساخت ویوی پاسخ به کامنتها
class PostAddReplyView(LoginRequiredMixin, View):
	form_class = CommentReplyForm

	def post(self, request, post_id, comment_id):
		post = get_object_or_404(Post, id=post_id)
		comment = get_object_or_404(Comment, id=comment_id)
		form = self.form_class(request.POST)
		if form.is_valid():
			reply = form.save(commit=False)
			reply.user = request.user
			reply.post = post
			reply.reply = comment
			reply.is_reply = True
			reply.save()
			messages.success(request, 'Your reply submitted successfully', 'success')
		return redirect('home:post_detail', post.id, post.slug)


# ویوی مربوط به لایک کردن پستها
class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'You have already liked this post!', 'danger')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'You liked this post.', 'success')
        return redirect('home:post_detail', post.id, post.slug)