from django.shortcuts import render,HttpResponseRedirect,redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template import loader,Context
from blog.models import UserTrack,Article,Category,Comment,User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.hashers import make_password,check_password
import datetime
import random
import json
from django import forms
from django.conf import settings

# Create your views here.
import logging



logger = logging.getLogger("blog.views")

class CommentForm(forms.Form):
    # pass
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'validate','id':'icon_prefix','required':'required','placeholder':'USERNAME'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'class':'validate','id':'email','placeholder':'EMAIL'}))
    cmt_content=forms.CharField(
        widget=forms.Textarea(attrs={'class':'materialize-textarea','id':'textarea1','required':'required','placeholder':'COMMENT CONTENT'}),
        error_messages={"required":"Comment can not be empty"}
    )
    # artcile_id = forms.CharField(widget=forms.HiddenInput())
    super_comment_id = forms.CharField(widget=forms.HiddenInput(attrs={'id':'super_comment_id'}))

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'validate','id':'login_email','placeholder':'LOGIN-EMAIL','required':'required'}),
                             error_messages={'required':'email 不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'validate','id':'login_password','placeholder':'PASSWORD','required':'required'}),
                               error_messages={'required': 'email 不能为空'}  )

class RegForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'regmail','id':'reg_email','placeholder':'EMAIL','onchange':'validate_email()'}),
                             error_messages={'required':'email 不能为空'},
                             required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'regpassword','id':'reg_password','placeholder':'PASSWORD',}),
                               error_messages={'required': 'password 不能为空'},
                               required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'regpassword2', 'id': 'reg_password2', 'placeholder': 'VALIDATION PASSWORD', 'onchange':'password_check()'}),
                               error_messages={'required': 'password2 不能为空'},
                                required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'regusername','id':'reg_username','placeholder':'USERNAME','required':'required','onchange':'validate_username()'}))

    desc = forms.CharField(widget=forms.Textarea(attrs={'class':'regdesc','id':'reg_desc','placeholder':'Description',}))
    chinese_name = forms.CharField(widget=forms.TextInput(attrs={'class':'regchinesename','id':'reg_chiniesename','placeholder':'ChineseName',}))
    # test = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'TEST'}),required=True)

def global_setting(request):
    article_list = Article.objects.all().order_by("-id")[:5]
    featured_post_list = article_list[:3]
    comment_list = Comment.objects.all()[:3]
    most_view_article = Article.objects.all().order_by("-click_count").first()
    login_status,username = session_login(request)
    login_email = request.session.get('login_email')
    return locals()



def session_login(request):
    # pass
    login_email = request.session.get('login_email',None)
    if  login_email  != None:
        user = User.objects.get(email=login_email)

        return 1,user.username
    return 0,None



'''
def to_page(request,page_name):
    try :
        remote_addr = request.META.get('REMOTE_ADDR', 'Not defined')
        http_user_agent = request.META.get('HTTP_USER_AGENT', 'Not defined')
        http_referer = request.META.get('HTTP_REFERER', 'Not defined')
        # track = UserTrack(remote_addr = remote_addr,http_user_agent=http_user_agent, http_referer=http_referer)
        track = UserTrack.create(remote_addr = remote_addr,http_user_agent=http_user_agent, http_referer=http_referer)
        print("================================== 111 " + request.META.get('SERVER_NAME','Not defined') )
        track.save()
        print("================================== " + track.remote_addr)
        # create_article()
    except Exception as e :
        logger.error(e)
    return render(request,page_name,locals())
'''

def paging(request,object_list,Object,rangelist):
    object_list = Object.objects.all()
    paginator = Paginator(object_list, 5)
    rangelist = [1, ]
    try:
        # pass
        page = paginator.page(request.GET.get("page", 1))
        object_list = paginator.page(page.number)
        page_num = 5
        if object_list.paginator.num_pages >= 1:
            if object_list.number + page_num <= object_list.paginator.num_pages:
                max_page = object_list.number + page_num
            else:
                max_page = object_list.paginator.num_pages + 1
            rangelist = range(object_list.number, max_page)
        else:
            rangelist = [1, ]
    except (EmptyPage, PageNotAnInteger, InvalidPage) as e:
        object_list = paginator.page(1)
        logger.error(e)
    return object_list,rangelist



def index_page(request):
    title = "Blog"
    # tarticle = Article.objects.get(id=100)
    home_article_list = rangelist = []
    home_article_list , rangelist = paging(request,home_article_list,Article,rangelist)
    return render(request,'index.html',locals())

def single_blog(request,article_id):
    single_article = Article.objects.get(id = article_id)
    single_article.click_count = single_article.click_count + 1
    single_article.save()
    all_comment_list = single_article.comment_set.all()
    article_comment_list = all_comment_list.filter( super_comment__isnull=True)
    sub_comment_list = all_comment_list.filter(super_comment__isnull=False)
    title = 'SINGLE BLOG'
    cmt_form = CommentForm()
    return render(request,'single-blog.html',locals())

def create_comment(request):
    cf = CommentForm(request.POST)
    login_email = request.session.get('login_email','')
    try:
        user=User.objects.get(email=login_email)
    except ObjectDoesNotExist as e:
        user = None
    article_id = request.POST.get('article_id',None)
    cmt_content = cf.data['cmt_content']
    username = cf.data['username']
    email = cf.data['email']
    super_comment_id = cf.data['super_comment_id']
    if super_comment_id =='' :
        super_comment_id = None
    else :
        super_comment_id = int(super_comment_id)

    article = Article.objects.get(id=article_id)
    comment = Comment(atc_id = article,
        cmt_content =cmt_content,
        super_comment = super_comment_id,
        username =username,
        user=user,
        email =email)
    comment.save()
    return HttpResponseRedirect(reverse("single_blog",args=[article_id]))

def json_test(request):
    # pass
    id = request.GET.get("article_id")
    article = Article.objects.get(id = id)
    article.like_count = article.like_count + 1
    article.save()

    print(id)
    dict = {"str":"testdata","like_count":article.like_count}
    dict = json.dumps(dict)
    return HttpResponse(dict)


def login_page(request):
    title="LoginPage"
    lf = LoginForm()
    return render(request,"login.html",locals())

def reg_page(request):
    title = "Register Page"
    rf = RegForm()
    return render(request, "register.html", locals())

def login_method(request,user,password):
    if check_password(password, user.password):
        # update the last login time.
        user.last_login = datetime.datetime.now()
        user.save()

        request.session['login_email'] = user.email
        request.session['user_id'] = user.id
        request.session['password'] = user.password
        return 1
    else:
        return 0

@csrf_exempt
def validate_login(request):
    title='Login'
    jsonmsg = {}
    lf = LoginForm(request.POST)
    lg_flag = 0
    jsonmsg['lg_flag'] = 0
    referer_url = request.POST.get("referer_url","")
    jsonmsg["referer_url"] = referer_url
    try:
        login_email = lf.data['email']
        password = lf.data['password']
        if lf.is_valid():
            try:
                user = User.objects.get(email=login_email)
                jsonmsg['lg_flag']= login_method(request, user, password)
                if jsonmsg['lg_flag'] == 0 :
                    jsonmsg['errormsg'] = '密码错误'
            except ObjectDoesNotExist as e:
                logger.error(e)
                jsonmsg['errormsg'] = "用户不存在"

        else:
            # raise forms.ValidationError("Message Errors")
            jsonmsg['errormsg'] = "账号或密码输入错误"
    except Exception as e:
        logger.error(e)
        jsonmsg['errormsg'] = "未知错误"
        return HttpResponse(json.dumps(jsonmsg))
    return HttpResponse(json.dumps(jsonmsg))

def validate_regemail(request):
    rf = RegForm(request.GET)
    email = request.GET.get('email',None)
    reg_valid = {}
    reg_valid['email_exists'] = 0
    if email :
        try:
            user=User.objects.get(email=email)
            reg_valid['email_exists'] = 1
        except ObjectDoesNotExist as e:
            pass
    return HttpResponse(json.dumps(reg_valid))

def validate_username(request):
    username = request.GET.get('username',None)
    reg_valid = {}
    reg_valid['username_exists'] = 0
    if username :
        try:
            user=User.objects.get(username=username)
            reg_valid['username_exists'] = 1
        except ObjectDoesNotExist :
            pass
    return HttpResponse(json.dumps(reg_valid))

@csrf_exempt
def commit_register(request):
    rf = RegForm(request.POST)
    jsonmsg={}
    jsonmsg['referer_url']=request.POST.get('referer_url')
    if rf.is_valid():
        email = rf.data['email']
        password = rf.data['password']
        username = rf.data['username']
        desc = rf.data['desc']
        chinese_name = rf.data['chinese_name']
        user = User(email=email,password=make_password(password),username=username,desc=desc,chinese_name=chinese_name)
        user.save()
        jsonmsg['lg_flag'] = login_method(request, user, password)
        if jsonmsg['lg_flag'] == 0:
            jsonmsg['errormsg'] = '密码错误'
    else:
        jsonmsg['errormsg'] = 'User created faild!'
        print(rf.errors)
        logger.error(rf.errors)
    return HttpResponse(json.dumps(jsonmsg))

def to_cateogry(request):
    return render(request, "cateogry.html", locals())

def to_contact(request):
    return render(request, "contact.html", locals())

def to_error(request):
    return render(request, "404.html", locals())

def session_test(request):
    # request.session['username'] = "TestUserName"
    name = request.session.get('username','NoUserName')
    return HttpResponse(name)

def logout(request):
    # pass
    request.session.flush()
    return redirect(reverse("blog"))
    # return HttpResponse(json.dumps(None))