from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import user_meta_form,card_form,meta_form
from django.contrib.auth import authenticate
from .models import user_meta,parts_model,categories_model,like_model,favorite_model,channel_model,afirieito_model,event_model,event_img_model,footer_cat_model,footer_model,tech_tube_model,tube_movie_model,tech_teaching_model,teaching_movie_model,bee_cate_model,bee_story_model
import requests
from django.contrib.auth.decorators import login_required
import os
from django.utils import timezone
from PIL import Image
import payjp
from django.core.paginator import Paginator
import time
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
import datetime
from django.utils.timezone import localtime
from django.core.signals import request_started
from django.core import signals
import cloudinary
import cloudinary.uploader
import cloudinary.api

def technext_view(request):
    return render(request,'techbee/indec2.html')

def my_error_handler(request, *args, **kw):
    import sys
    from django.views import debug
    from django.http import HttpResponse
    params={
        'e':'',
    }
    return render(request,'techbee/500.html',params)


def status_veri(user):
    try:
        meta=user_meta.objects.get(user=user)
    except:
        return True
    try:
        posi=meta.position
    except:
        return True
    else:
        if posi == 'paypal':
            return False
        else:
            return True



def login_bonus(user):
    login_date=user.user_meta.last_login
    login_month=login_date.month
    login_day=login_date.day
    now=datetime.date.today()
    now_month=now.month
    now_day=now.day
    if (login_date.day != now.day) or (login_month != now_month):
        meta=user_meta.objects.get(user=user)
        meta.last_login=datetime.date.today()
        meta.like_point += 33
        afi=afirieito_model.objects.filter(introducer=user.user_meta.username)
        afi_list=0
        for i in afi:
            u_meta=user_meta.objects.get(user=i.user)
            if u_meta.position =='paypal':
                afi_list +=1
        afi_len=int(afi_list)*33
        meta.point += afi_len
        meta.save()

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# ページネーション用に、Pageオブジェクトを返す。
def paginate_query(request, queryset, count):
  paginator = Paginator(queryset, count)
  page = request.GET.get('page')
  try:
    page_obj = paginator.page(page)
  except PageNotAnInteger:
    page_obj = paginator.page(1)
  except EmptyPage:
    page_obj = paginator.page(paginator.num_pages)
  return page_obj



def error404_view(request):
    return render(request,'404.html')

def logout_view(request):
    logout(request)
    return redirect(to='index')
import datetime

@login_required
def index(request):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    login_bonus(user)
    b_cate=bee_cate_model.objects.all()

    params={
        'index_current':request.path,
        'aaa':'',
        'bbb':b_cate,
        }
    return render(request,'techbee/index.html',params)

@login_required
def tb_view(request,cate):
    payjp.api_key ='sk_test_f0d6fe8a9725200cda316d56'
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    login_bonus(user)
    b_cate=bee_cate_model.objects.get(category=cate)
    b_story=bee_story_model.objects.filter(category=b_cate)
    params={
        'cate':cate,
        'ccc':b_story,
    }
    return render(request,'techbee/tech-bee.html',params)

@login_required
def tech_view(request,category,w,num):
    params={
        'top':'',
        'site_name':settings.SITE_NAME,
        'page_obj':'',
        't_title':'',
        'category_l':'',
        'category_f':'',
        'category_len':'',
        'category':category,
        'w':w,
    }
    if category == 'movie':
        t_title='TechMovie'
        params['t_title']=t_title
        if num == 0:
            top=tube_movie_model.objects.latest('post_time')
            params['top']=top
        else:
            top=tube_movie_model.objects.get(id=num)
            params['top']=top
        if w == 0:
            new=tube_movie_model.objects.all().order_by('-post_time')
            page_obj = paginate_query(request, new, settings.PAGE_PER_ITEM)
            params['page_obj']=page_obj
        else:
            cate=tech_tube_model.objects.all()
            page_obj = paginate_query(request, cate, settings.PAGE_PER_ITEM)
            params['page_obj']=page_obj
        if top.category != None:
            try:
                category=tube_movie_model.objects.filter(category=top.category)
                category_f=category.order_by('-post_time')
                category_l=category.order_by('post_time')
            except:
                pass
            else:
                for c in category_f:
                    if top.post_time > c.post_time:
                        params['category_f']=c
                        break
                for c in category_l:
                    if top.post_time < c.post_time:
                        params['category_l']=c
                        break
                global category_len
                params['category_len']=len(category)
        else:
            params['category_len']=0

    elif category == 'teaching':
        t_title='TechTeaching'
        params['t_title']=t_title
        if num == 0:
            top=teaching_movie_model.objects.latest('post_time')
            params['top']=top
        else:
            top=teaching_movie_model.objects.get(id=num)
            params['top']=top
        if w == 0:
            new=teaching_movie_model.objects.all().order_by('-post_time')
            page_obj = paginate_query(request, new, settings.PAGE_PER_ITEM)
            params['page_obj']=page_obj
        else:
            cate=tech_teaching_model.objects.all()
            page_obj = paginate_query(request, cate, settings.PAGE_PER_ITEM)
            params['page_obj']=page_obj
        if top.category != None:
            try:
                category=teaching_movie_model.objects.filter(category=top.category)
                category_f=category.order_by('-post_time')
                category_l=category.order_by('post_time')
            except:
                pass
            else:
                for c in category_f:
                    if top.post_time > c.post_time:
                        params['category_f']=c
                        break
                for c in category_l:
                    if top.post_time < c.post_time:
                        params['category_l']=c
                        break
                params['category_len']=len(category)
        else:
            params['category_len']=0

    return render(request,'techbee/tech.html',params)


@login_required
def tech_series_view(request,category,num):
    params={
        'category':category,
        'num':num,
        'page_obj':'',
        'c_model':'',
        't_title':'',

    }
    if category == 'movie':
        t_title='TechMovie'
        params['t_title']=t_title
        cate=tech_tube_model.objects.get(id=num)
        params['c_model']=cate
        obj=tube_movie_model.objects.filter(category=cate)
        page_obj = paginate_query(request, obj, settings.PAGE_PER_ITEM)
        params['page_obj']=page_obj
    else:
        t_title='TechTeaching'
        params['t_title']=t_title
        cate=tech_teaching_model.objects.get(id=num)
        params['c_model']=cate
        obj=teaching_movie_model.objects.filter(category=cate)
        page_obj = paginate_query(request, obj, settings.PAGE_PER_ITEM)
        params['page_obj']=page_obj

    return render(request,'techbee/techseries.html',params)





@login_required
def login_select_view(request):
    user = request.user
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)

    login_bonus(user)
    try:
        user.user_meta.username
    except:
        params={
        'username_form':user_meta_form()
        }
        return render(request,'techbee/userregi.html',params)
    else:
        payjp.api_key ='sk_test_f0d6fe8a9725200cda316d56'
        customer = payjp.Customer.retrieve(user.user_meta.username)
        user_status=customer["subscriptions"]["data"][0]['status']
        params={
        'aaa':user_status,
        'index_current':request.path,
        }
        if status_veri(user)==True:
            return render(request,'techbee/statusveri.html')
        return render(request,'techbee/index.html',params)

@login_required
def userregi_view(request,introducer):
    user=request.user
    try:
        afirieito_model.objects.get(user=user)
    except:
        afirieito_model(user=user,introducer=introducer).save()
    payjp.api_key ='sk_test_f0d6fe8a9725200cda316d56'
    if request.method=='POST':
        position=request.POST['position']
        try:
            username=request.POST['username']
        except:
            username=user.user_meta.username

        try:
            meta=user_meta.objects.get(user=user)
        except:
            user_meta(user=user,username=username,position=position).save()
        else:
            meta.position=position
            meta.save()

        return redirect(to='paypal')

    try:
        user.user_meta
    except:
        m=False
    else:
        m=True
    params={
        'introducer':introducer,
        'm':m,
    }
    return render(request,'techbee/userregi.html',params)

@login_required
def paypal_view(request):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    meta=user_meta.objects.get(user=user)
    if meta.position=='member':
        return render(request,'techbee/paypal.html')
    else:
        return render(request,'techbee/paypal2.html')


def paypal_complete_view(request):
    user=request.user
    try:
        meta=user_meta.objects.get(user=user)
        meta.username
    except:
        return redirect('technext')
    else:
        meta.position = 'paypal'
        meta.save()
        return redirect(to='after')

def paypal_after_view(request):
    return render(request,'techbee/after.html')


from operator import itemgetter
@login_required
def parts_search_view(request,search_kind):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    catelist=categories_model.objects.filter(user=user)
    search_path="/techbee/parts/"+str(search_kind)+'/'
    params={
        'page_obj':'',
        'site_name':'',
        'search_kind':search_kind,
        'search_path':search_path,
        'rrr':catelist,
    }
    if search_kind == 'new':
        obj=parts_model.objects.all().order_by('-post_time')
        page_obj = paginate_query(request, obj, settings.PAGE_PER_ITEM)
        params['site_name']=settings.SITE_NAME
        params['page_obj']=page_obj
    elif search_kind == 'like':
        obj=parts_model.objects.all().order_by('-like_count')
        page_obj = paginate_query(request, obj, settings.PAGE_PER_ITEM)
        params['site_name']=settings.SITE_NAME
        params['page_obj']=page_obj
    elif search_kind == 'list':
        aaa_list=[]
        obj=categories_model.objects.all()
        post_list=[]
        for a in obj:
            partlen=parts_model.objects.filter(categories=a)
            if len(partlen) > 0:
                total_like=0
                for p in partlen:
                    total_like += p.like_count
                post_d=(a.categories,total_like)
                post_list.append(post_d)
        post_dict=dict(post_list)
        sort1 = sorted(post_dict, key=itemgetter(1),reverse=True)
        for item in sort1:
            c=categories_model.objects.get(categories=item)
            aaa_list.append(c)
        page_obj = paginate_query(request, aaa_list, settings.PAGE_PER_ITEM)
        params['site_name']=settings.SITE_NAME
        params['page_obj']=page_obj
    elif search_kind == 'random':
        obj=parts_model.objects.all().order_by('?')
        page_obj = paginate_query(request, obj, settings.PAGE_PER_ITEM)
        params['site_name']=settings.SITE_NAME
        params['page_obj']=page_obj

    return render(request,'techbee/parts.html',params)

@login_required
def parts_part_view(request,username,id):
    user = request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    if status_veri(user)==True:
        return render(request,'techbee/statusveri.html')
    else:
        try:
            part=parts_model.objects.get(id=id)
            obj=parts_model.objects.all().order_by('-post_time')
            like=like_model.objects.filter(user=user,part_id=part)
            favorite=favorite_model.objects.filter(user=user,part_id=part)
            meta=user_meta.objects.get(username=username)
            channel=channel_model.objects.filter(user=user,username=meta.user)
            catelist=categories_model.objects.filter(user=user)
        except:
            return render(request,'404.html')

        if username == user.user_meta.username:
            openuser='userself'
        else:
            openuser='another'
        params={
            'user_like':int(user.user_meta.like_point),
            'look':openuser,
            'part':part,
            'aaa':username,
            'category_len':'',
            'category_f':'',
            'category_l':'',
            'liked':len(like),
            'favorite':len(favorite),
            'channel':len(channel),
            'res':'',
            'rrr':catelist,
        }
        if part.categories != None:
            try:
                category=parts_model.objects.filter(user=part.user,categories=part.categories)
                category_f=category.order_by('-post_time')
                category_l=category.order_by('post_time')
            except:
                pass
            else:
                for c in category_f:
                    if part.post_time > c.post_time:
                        params['category_f']=c
                        break
                for c in category_l:
                    if part.post_time < c.post_time:
                        params['category_l']=c
                        break
                params['category_len']=len(category)
        else:
            params['category_len']=0
    return render(request,'techbee/par2.html',params)

@login_required
def parts_list_view(request,username,categories_id):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    meta=user_meta.objects.get(username=username)
    cate=categories_model.objects.get(id=categories_id)
    part=parts_model.objects.filter(user=meta.user,categories=cate)
    channel=channel_model.objects.filter(user=request.user,username=meta.user)
    catelist=categories_model.objects.filter(user=user)
    page_obj = paginate_query(request, part, settings.PAGE_PER_ITEM)   # ページネーション
    if username == user.user_meta.username:
        openuser='userself'
    else:
        openuser='another'
    params={
        'look':openuser,
        'list':cate,
        'page_obj':page_obj,
        'channel':len(channel),
        'rrr':catelist,
        'site_name':settings.SITE_NAME,
    }
    return render(request,'techbee/par3.html',params)

@login_required
def accountkind_view(request,username,kind):
    user = request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    meta=user_meta.objects.get(username=username)
    channel=channel_model.objects.filter(user=user,username=meta.user)
    catelist=categories_model.objects.filter(user=user)
    if username == user.user_meta.username:
        openuser='userself'
    else:
        openuser='another'
    params={
        'user':user,
        'look':openuser,
        'account_current':request.path,
        'username':username,
        'topPhoto':meta.photo,
        'name':meta.name,
        'plofile':meta.plofile,
        'point':meta.point,
        'like_point':meta.like_point,
        'kind':kind,
        'list_len':'',
        'channel':len(channel),
        'meta_form':meta_form(),
        'rrr':catelist,
        'mmm':'',
        'page_obj':'',
        'site_name':'',


        }
    if kind == 'post':
        meta=user_meta.objects.get(username=username)
        post_contents=parts_model.objects.filter(user=meta.user).order_by('-post_time')
        page_obj = paginate_query(request, post_contents, settings.PAGE_PER_ITEM)   # ページネーション
        params['page_obj']= page_obj
        params['site_name']=settings.SITE_NAME
    elif kind == 'list':
        meta=user_meta.objects.get(username=username)
        post_contents=categories_model.objects.filter(user=meta.user).order_by('-post_time')
        if openuser == 'userself':
            page_obj = paginate_query(request, post_contents, settings.PAGE_PER_ITEM)
            params['page_obj']= page_obj
            params['site_name']=settings.SITE_NAME
        else:
            post_list=[]
            for a in post_contents:
                partlen=parts_model.objects.filter(categories=a)
                if len(partlen) > 0:
                    post_list.append(a)
            page_obj = paginate_query(request, post_list, settings.PAGE_PER_ITEM)
            params['page_obj']= page_obj
            params['site_name']=settings.SITE_NAME
            params['list_len']=parts_model.objects.filter(user=meta.user)
    elif kind =='favorite':
        meta=user_meta.objects.get(username=username)
        post_contents=favorite_model.objects.filter(user=meta.user).order_by('-favorite_time')
        post_list=[]
        for a in post_contents:
            part=a.part_id
            post_list.append(part)
        page_obj = paginate_query(request, post_list, settings.PAGE_PER_ITEM)
        params['page_obj']= page_obj
        params['site_name']=settings.SITE_NAME
    elif kind == 'channel':
        meta=user_meta.objects.get(username=username)
        post_contents=channel_model.objects.filter(user=meta.user).order_by('-channel_time')
        post_list=[]
        for a in post_contents:
            part=user_meta.objects.get(user=a.username)
            post_list.append(part)
        page_obj = paginate_query(request, post_list, settings.PAGE_PER_ITEM)
        params['page_obj']= page_obj
        params['site_name']=settings.SITE_NAME
    elif kind == 'member':
        meta=user_meta.objects.get(username=username)
        afi=afirieito_model.objects.filter(introducer=user.user_meta.username)
        member_list=[]
        for a in afi:
            member=user_meta.objects.get(user=a.user)
            member_list.append(member)
        page_obj = paginate_query(request, member_list, settings.PAGE_PER_ITEM)
        params['page_obj']= page_obj
        params['site_name']=settings.SITE_NAME
    return render(request,'techbee/account.html',params)

def metapost_view(request):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    username=user.user_meta.username
    kind='post'
    if request.method=='POST':
        name=request.POST['name']
        plofile=request.POST['plofile']
        g_like=request.POST['g_like']
        user_m=user_meta.objects.get(user=user)
        try:
            photo=request.FILES['photo']
        except:
            pass
        else:
            cloudinary.uploader.destroy(user_m.photo.public_id)
            user_m.photo=photo
        if name!='':
            user_m.name=name
        user_m.give_like=g_like
        user_m.plofile=plofile
        user_m.save()
    return redirect('accountkind',user.user_meta.username,'post')

@login_required
def community_view(request):
    user = request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    catelist=categories_model.objects.filter(user=user)
    event=event_model.objects.all().order_by('-set_event')
    page_obj = paginate_query(request, event, 10)
    payjp.api_key ='sk_test_f0d6fe8a9725200cda316d56'
    customer = payjp.Customer.retrieve(user.user_meta.username)

    if status_veri(user)==True:
        params={
            'p':customer["subscriptions"]["data"][0]['status'],
        }
        return render(request,'techbee/statusveri.html',params)
    else:
        params={
            'eee':event,
            'rrr':catelist,
            'page_obj':page_obj,
            'site_name':settings.SITE_NAME,
        }
        return render(request,'techbee/community.html',params)
@login_required
def community2_view(request,id):
    user = request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    catelist=categories_model.objects.filter(user=user)
    event=event_model.objects.get(id=id)
    payjp.api_key ='sk_test_f0d6fe8a9725200cda316d56'
    customer = payjp.Customer.retrieve(user.user_meta.username)
    img=event_img_model.objects.filter(event=event).order_by('-img')
    page_obj = paginate_query(request, img, settings.PAGE_PER_ITEM)
    user_img=event_img_model.objects.filter(user=user,event=event)
    if status_veri(user)==True:
        params={
            'p':customer["subscriptions"]["data"][0]['status'],
        }
        return render(request,'techbee/statusveri.html',params)
    else:
        params={
            'e':event,
            'page_obj':page_obj,
            'site_name':settings.SITE_NAME,
            'aaa':user_img,
            'rrr':catelist,

        }
        return render(request,'techbee/community2.html',params)


def footer_view(request,category):
    params={
        'category':category,
        'f_cate':'',
    }
    try:
        fc_model=footer_cat_model.objects.get(footer_cat=category)
    except:
        pass
    else:
        f_cate=footer_model.objects.filter(footer_cat=fc_model)
        params['f_cate']=f_cate
    return render(request,'techbee/footer.html',params)

@login_required
def album_view(request,id):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if request.method=='POST':
        try:
            photo_list=request.FILES.getlist('photo')
        except:
            pass
        else:
            event=event_model.objects.get(id=id)
            for value in photo_list:
                event_img_model(user=user,event=event,img=value).save()
        try:
            on=request.POST
        except:
            pass
        else:
            on=tuple(on.items())
            for key,value in on:
                if 'check' in key:
                    event_img=event_img_model.objects.get(id=int(value))
                    cloudinary.uploader.destroy(event_img.img.public_id)
                    event_img.delete()
    return redirect('community_event',id)

@login_required
def ranking_view(request):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    obj=user_meta.objects.all().order_by('-point')
    ooo=[]
    o_count=0
    for o in obj:
        o_count+=1
        if o_count > 10:
            ooo.append(o)
    page_obj = paginate_query(request, ooo, settings.PAGE_PER_ITEM)
    catelist=categories_model.objects.filter(user=user)
    params={
        'aaa':obj,
        'rrr':catelist,
        'page_obj':page_obj,
        'site_name':settings.SITE_NAME,
    }
    return render(request,'techbee/ranking.html',params)



def touko_view(request):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    if request.method=='POST':
        try:
            newseries=request.POST['newseries']
        except:
            newseries=''
        try:
            categories=request.POST['categories']
        except:
            categories=''
        filename=request.POST['filename']
        image=request.FILES['tokoImage']
        codepen=request.POST['codepen']
        text=request.POST['text']
        if newseries != '':
            try:
                cate=categories_model.objects.get(user=user,categories=newseries)
            except:
                categories_model(user=user,categories=newseries).save()
                cate=categories_model.objects.get(user=user,categories=newseries)
                parts_model(user=user,categories=cate,file_name=filename,image=image,codepen=codepen,text=text).save()
            else:
                parts_model(user=user,categories=cate,file_name=filename,image=image,codepen=codepen,text=text).save()
        elif categories != '':
            cate=categories_model.objects.get(user=user,categories=categories)
            parts_model(user=user,categories=cate,file_name=filename,image=image,codepen=codepen,text=text).save()
        else:
            parts_model(user=user,categories=None,file_name=filename,image=image,codepen=codepen,text=text).save()
        newpart=parts_model.objects.filter(user=user).order_by('-post_time')
        part=parts_model.objects.get(id=newpart[0].id)
        obj=parts_model.objects.all().order_by('-post_time')
        like=like_model.objects.filter(user=user,part_id=newpart[0].id)
        favorite=favorite_model.objects.filter(user=user,part_id=newpart[0].id)
        channel=channel_model.objects.filter(user=user,username=user)
        catelist=categories_model.objects.filter(user=user)
        openuser='userself'
        params={
            'look':openuser,
            'part':part,
            'aaa':user.user_meta.username,
            'category_len':'',
            'category_f':'',
            'category_l':'',
            'liked':len(like),
            'favorite':len(favorite),
            'channel':len(channel),
            'res':'',
            'rrr':catelist,
        }
        if part.categories!=None:
            try:
                category=parts_model.objects.filter(user=part.user,categories=part.categories)
                category_f=category.order_by('-post_time')
                category_l=category.order_by('post_time')
            except:
                pass
            else:
                for c in category_f:
                    if part.post_time > c.post_time:
                        params['category_f']=c
                        break
                for c in category_l:
                    if part.post_time < c.post_time:
                        params['category_l']=c
                        break
                params['category_len']=len(category)
        else:
            params['category_len']=0
    return render(request,'techbee/par2.html',params)


def editsave_view(request,username,id):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    if request.method=='POST':
        try:
            newseries=request.POST['newseries_edit']
        except:
            newseries=''
        try:
            categories=request.POST['categories_edit']
        except:
            categories=''
        filename=request.POST['filename_edit']
        text=request.POST['text']
        part_edit=parts_model.objects.get(id=id)
        if newseries != '':
            try:
                cate=categories_model.objects.get(user=user,categories=newseries)
            except:
                categories_model(user=user,categories=newseries).save()
                cate=categories_model.objects.get(user=user,categories=newseries)
                part_edit.categories=cate
                part_edit.file_name=filename
                part_edit.text=text
                part_edit.save()
            else:
                part_edit.categories=cate
                part_edit.file_name=filename
                part_edit.text=text
                part_edit.save()
        elif categories != '':
            cate=categories_model.objects.get(user=user,categories=categories)
            part_edit.categories=cate
            part_edit.file_name=filename
            part_edit.text=text
            part_edit.save()
        else:
            part_edit.categories=None
            part_edit.file_name=filename
            part_edit.text=text
            part_edit.save()
        newpart=parts_model.objects.filter(user=user).order_by('-post_time')
        part=parts_model.objects.get(id=id)
        obj=parts_model.objects.all().order_by('-post_time')
        like=like_model.objects.filter(user=user,part_id=newpart[0].id)
        favorite=favorite_model.objects.filter(user=user,part_id=newpart[0].id)
        channel=channel_model.objects.filter(user=user,username=user)
        catelist=categories_model.objects.filter(user=user)
        openuser='userself'
        params={
            'look':openuser,
            'part':part,
            'aaa':user.user_meta.username,
            'category_len':'',
            'category_f':'',
            'category_l':'',
            'liked':len(like),
            'favorite':len(favorite),
            'channel':len(channel),
            'res':'',
            'rrr':catelist,
        }
        if part.categories!=None:
            try:
                category=parts_model.objects.filter(user=part.user,categories=part.categories)
                category_f=category.order_by('-post_time')
                category_l=category.order_by('post_time')
            except:
                pass
            else:
                for c in category_f:
                    if part.post_time > c.post_time:
                        params['category_f']=c
                        break
                for c in category_l:
                    if part.post_time < c.post_time:
                        params['category_l']=c
                        break
                params['category_len']=len(category)
        else:
            params['category_len']=0
    return render(request,'techbee/par2.html',params)

def toukoedit_view(request,username,id):
    user = request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    part=parts_model.objects.get(id=id)
    catelist=categories_model.objects.filter(user=user)
    if username == user.user_meta.username:
        openuser='userself'
    else:
        openuser='another'
    params={
        'look':openuser,
        'part':part,
        'aaa':username,
        'category_len':'',
        'category_f':'',
        'category_l':'',
        'rrr':catelist,
    }
    if part.categories != None:
        try:
            category=parts_model.objects.filter(user=part.user,categories=part.categories)
            category_f=category.order_by('-post_time')
            category_l=category.order_by('post_time')
        except:
            pass
        else:
            for c in category_f:
                if part.post_time > c.post_time:
                    params['category_f']=c
                    break
            for c in category_l:
                if part.post_time < c.post_time:
                    params['category_l']=c
                    break
            params['category_len']=len(category)
    else:
        params['category_len']=0

    return render(request,'techbee/edit.html',params)

def delete_cate_view(request):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    if request.method=='POST':
        list_id=request.POST['list_id']
        delete_list=categories_model.objects.get(id=list_id)
        cloudinary.uploader.destroy(delete_list.img.public_id)
        delete_list.delete()

    return redirect('accountkind',user.user_meta.username,'list')

def delete_part_view(request,username,id):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    part=parts_model.objects.get(id=id)
    if user.user_meta.username==username:
        cloudinary.uploader.destroy(part.image.public_id)
        part.delete()
    return redirect('accountkind',user.user_meta.username,'post')

def editcate_view(request,username,id):
    user=request.user
    try:
        user.user_meta.username
    except:
        return redirect(to='loginselect')
    if status_veri(user)==True:
        a=afirieito_model.objects.get(user=user)
        params={
            'a':a,
        }
        return render(request,'techbee/statusveri.html',params)
    login_bonus(user)
    if request.method=='POST':
        cate=categories_model.objects.get(id=id)
        try:
            photo=request.FILES['photo']
        except:
            pass
        else:
            cloudinary.uploader.destroy(cate.img.public_id)
            cate.img=photo
            cate.save()
        try:
            categories=request.POST['seriesname']
        except:
            pass
        else:
            cate.categories=categories
            cate.save()
    return redirect('partslist',user.user_meta.username,id)



def like_ajax_response(request):
    if request.method=='POST':
        input_user = request.user
        input_part = request.POST['part_id']
        partmodel=parts_model.objects.get(id=int(input_part))
        like=like_model.objects.filter(user=input_user,part_id=partmodel)
        meta=user_meta.objects.get(user=input_user)
        part_meta=user_meta.objects.get(user=partmodel.user)
        if len(like) == 0 and int(input_user.user_meta.give_like) <= int(input_user.user_meta.like_point):
            like_model(user=input_user,part_id=partmodel).save()
            meta.like_point -= int(input_user.user_meta.give_like)
            meta.point += int(input_user.user_meta.give_like)
            meta.save()
            part_meta.point += int(input_user.user_meta.give_like)
            part_meta.save()
            partmodel.like_count += int(input_user.user_meta.give_like)
            partmodel.save()
            res='Success to like'
        else :
            try:
                likes=like_model.objects.get(user=input_user,part_id=partmodel)
                liket=likes.like_time.timestamp()
                timen=timezone.datetime.now().timestamp()
                a=timen-liket
            except:
                res='s'
            else:
                if a <600:
                    like.delete()
                    meta.like_point += int(input_user.user_meta.give_like)
                    meta.point -= int(input_user.user_meta.give_like)
                    meta.save()
                    part_meta.point -= int(input_user.user_meta.give_like)
                    part_meta.save()
                    partmodel.like_count -= int(input_user.user_meta.give_like)
                    partmodel.save()
                    res='Success to unlike'
                else:
                    re='a'
    return HttpResponse(res)

def favorite_ajax_view(request):
    if request.method=='POST':
        input_user = request.user
        input_part = request.POST['part_id']
        partmodel=parts_model.objects.get(id=input_part)
        favorite=favorite_model.objects.filter(user=input_user,part_id=partmodel)
        if len(favorite) == 0:
            favorite_model(user=input_user,part_id=partmodel).save()
            res='Success to favorite'
        else:
            favorite.delete()
            res='Success to unfavotire'
    return HttpResponse(res)

def channel_ajax_view(request):
    if request.method=='POST':
        input_user = request.user
        input_username = request.POST['username']
        meta=user_meta.objects.get(username=input_username)
        channel=channel_model.objects.filter(user=input_user,username=meta.user)
        if len(channel) == 0:
            channel_model(user=input_user,username=meta.user).save()
            res='登録完了'
        else:
            channel.delete()
            res='Success to unchannel'
    return HttpResponse(res)


##########################################################
#API
import django_filters
from rest_framework import viewsets, filters

from .serializer import LikeSerializer,FavoriteSerializer,ChannelSerializer
class LikeViewSet(viewsets.ModelViewSet):
    queryset = like_model.objects.all()
    serializer_class = LikeSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = favorite_model.objects.all()
    serializer_class = FavoriteSerializer

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = channel_model.objects.all()
    serializer_class = ChannelSerializer
##########################################################
