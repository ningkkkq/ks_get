from django.shortcuts import render, redirect, reverse
# Create your views here.


def index(request):
    try:
        if request.COOKIES.get('status') or request.session.get('status'):
            return render(request, 'index.html')
        else:
            return redirect(reverse('NeedLogin:login'))
    except:
        return redirect(reverse('NeedLogin:login'))


def logout(request):
    resp = redirect(reverse('NeedLogin:login'))
    try:
        resp.delete_cookie('status')
    except:
        try:
            del request.session["status"]
        except:
            print('未删除成功。。')
    finally:
        return resp
