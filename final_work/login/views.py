from django.shortcuts import render, redirect, reverse
from login.models import *


# Create your views here.


def login(request):
    try:
        # 带有cookie直接放行
        if request.COOKIES.get('status'):
            return redirect(reverse('PlayVideo:getStart'))
        else:
            raise Exception('get None in cookies')
    except:
        if request.method == 'POST':
            try:
                # 验证账户密码设置cookie
                ret = User.objects.get(uid=request.POST.get('uid'))
                if ret.password == request.POST.get('password'):
                    if request.POST.get('remember') == 'on':
                        print('我在设置session')
                        rep = redirect('/play/')
                        rep.set_cookie('status', True, 120)
                        return rep
                    else:
                        rep = redirect('/play/')
                        request.session['status'] = True
                        return rep
                else:
                    raise Exception('wrong password')
            except:
                return render(request, 'login.html', {'msg': '密码错误或出现异常！'})
        return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        try:
            # 将数据存储到数据库，返回登录页面
            ret = User.objects.get(uid=request.POST.get('uid'))
            if ret:
                return render(request, 'signup.html', {'msg': '用户已存在！'})
            item = User(uid=request.POST.get('uid'), password=request.POST.get('password'))
            item.save()
            return redirect(reverse('NeedLogin:login'))
        except:
            return render(request, 'signup.html')
    return render(request, 'signup.html')
