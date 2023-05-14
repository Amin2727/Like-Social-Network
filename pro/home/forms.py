from django import forms
from .models import Post, Comment

# مربوط به جلسه ی ۲۲ برای آپدیت فرم ساختیم که ازش در ویوش استفاده کنیم
# در جلسه ۲۴ میایم کریت هم قبل از آپدیت میذاریم در اسم کلاس چون جفت فرمها هم برای آپدیت و هم برای کریت یکیه
class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


# این مربوط به جلسه ی ۳۷ دوره هستش که میاد یک فرمی رو برای پاسخ به کامنتها ایجاد میکنه که کاربری که براش کامنت اومده اگه خواست جواب بده به کامنتها ازش استفاده کنه
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
			'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Type your comment.'})
		}


# مربوط به جلسه ی ۳۹ هستش که میاد فرم مربوط به جواب کامنت رو میسازیم
class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
			'body': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Type your response.'})
		}


# مربوط به جلسه ی ۴۱ دوره ساخت فرم سرچ کردن هستش
class PostSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'size':'30'}))