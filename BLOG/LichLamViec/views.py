from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from django.db import connection
from django.core import serializers
import json

# Create your views here.

tmp = TK_tmp()
def homepage(request):
    tuan = Tuan.objects.get(sd=0)
    MK_xemlich = MatKhauXemLich.objects.get(id=1)
    id = tuan.id
    t2 = Thu2.objects.filter(id_tuan=id)
    t3 = Thu3.objects.filter(id_tuan=id)
    t4 = Thu4.objects.filter(id_tuan=id)
    t5 = Thu5.objects.filter(id_tuan=id)
    t6 = Thu6.objects.filter(id_tuan=id)
    t7 = Thu7.objects.filter(id_tuan=id)
    cn = ChuNhat.objects.filter(id_tuan=id)
    if MK_xemlich.sd == 1:
        display = 'block'
    else:
        display = 'none'

    print(MK_xemlich.sd)
    return render(request, 'index.html', {'t2': t2, 't3': t3, 't4': t4, 't5': t5, 't6': t6, 't7': t7, 'cn': cn, 'display':display,'MK': MK_xemlich})

def showLoginForm(request):
    return render(request, 'login.html')

def changepass(request):
    info = ''
    color = 'red'
    if request.method == 'POST':
        tk = request.POST['usr']
        MKC = request.POST['MKC']
        MKM = request.POST['pwd']
        XacNhanMK = request.POST['XacNhanMK']
        TK = TaiKhoan.objects.filter(id=1)
        if tk == TK[0].usr and MKC == TK[0].pwd:
            if MKM != '':
                if MKM == XacNhanMK:
                    TK.update(pwd=MKM)
                    return redirect('../login')
                else:
                    info = 'Mật khẩu xác nhận không đúng!'
            else:
                info = 'Vui lòng nhập mật khẩu mới!'
        else:
            print(TK[0].usr)
            print(TK[0].pwd)
            print(TK)
            info = 'Tài khoản hoặc mật khẩu cũ không chính xác!'

    return render(request, 'changepass.html', {'info': info, 'color': color})

def changemail(request):
    info = ''
    color = 'red'
    TK = TaiKhoan.objects.filter(id=1)
    if request.method == 'POST':
        mail = request.POST['mail']
        if mail != '':
           TK.update(mail=mail)
           info = 'Thay đổi mail thành công!'
           color = 'green'
           return render(request, 'changemail.html', {'info': info, 'color': color, 'mail': TK[0].mail})
        else:
             info = 'Vui lòng nhập mail!'

    return render(request, 'changemail.html', {'info': info, 'color': color, 'mail': TK[0].mail})

def calendar_pass(request):
    info = ''
    color = 'red'
    check1 = ''
    check2 = ''
    MK = MatKhauXemLich.objects.filter(id=1)
    if request.method == 'POST':
        mk = request.POST['pwd']
        input_sd = request.POST['sd']
        if mk != '':
            if input_sd == '1':
                MK.update(MatKhau=mk, sd=input_sd)
            else:
                MK.update(MatKhau=mk, sd=0)

            info = 'Thay đổi mật khẩu thành công!'
            color = 'green'

        else:
             info = 'Vui lòng nhập mail!'


    sd = MK[0].sd
    if sd == 1:
        check1 = 'checked'
    else:
        check2 = 'checked'
    return render(request, 'calendar_pass.html', {'info': info, 'color': color, 'mk': MK[0].MatKhau,
                                                  'check1' : check1, 'check2' : check2})

def logout(request):
    tmp.setTK('')
    tmp.setMK('')
    print(tmp.getTK())
    return redirect('../login')

def login(request):
    TK = TaiKhoan.objects.all()
    if request.method == 'POST':
        usr = request.POST['usr']
        pwd = request.POST['pwd']
        if (usr == TK[0].usr) and (pwd == TK[0].pwd):
            tuan = Tuan.objects.all()
            tmp.setTK(TK[0].usr)
            tmp.mk = TK[0].pwd
            print(tmp.getTK())

            return render(request, 'admin_home.html', {'tuan': tuan})
    else:
        print(tmp.getTK())
        if (tmp.tk == TK[0].usr) and (tmp.mk == TK[0].pwd):
            tuan = Tuan.objects.all()
            return render(request, 'admin_home.html', {'tuan': tuan})
        return redirect('../login')
    return redirect('../login')


def updatet2(request, id):
    info = ''
    t2 = Thu2.objects.get(id=id)
    #lay id tuan tu bang thu2
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        print('Tieu de la'+TieuDe)

        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if check_timedelta(BD, KT) == True:
                    Thu2.objects.get(id=id).delete()
                    if max_date_update('thu2', BD, KT) == True:
                        tt = Thu2(id=id, ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung,
                                  id_tuan=t2.id_tuan)
                        tt.save()
                    else:
                        print(TieuDe)
                        tt1 = Thu2(id=id, ThoiGianBD=t2.ThoiGianBD, ThoiGianKT=t2.ThoiGianKT, TieuDe=t2.TieuDe, NoiDung=t2.NoiDung,
                                   id_tuan=t2.id_tuan)
                        tt1.save()
                        info = "Bạn chưa cập nhật thời gian thành công do thời gian này đã được sử dụng!"
                else:
                    info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'

            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    return render(request, 'admin_update.html', {'thu': t2, 'day':'t2', 'info':info})

def addt2_show(request, id):
    print('Dang chay addt2_show')
    return render(request, 'admin_add.html', {'id_tuan':id, 'thu':'t2'})

def addt2(request, id):
    tuan = Tuan.objects.get(id=id)
    info = ''
    print("Dang chay addt2")
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if max_date_update('thu2', BD, KT) == True:
                    if check_timedelta(BD, KT) == True:
                        tt = Thu2(ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung, id_tuan=tuan)
                        tt.save()
                    else:
                        info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'
                else:
                    info = "Thời gian này đã được sử dụng!"
            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    return render(request, 'admin_add.html', {'id_tuan':id, 'thu':'t2', 'info':info})

def addt3(request, id):
    info = ''
    tuan = Tuan.objects.get(id=id)
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if max_date_update('thu3', BD, KT) == True:
                    if check_timedelta(BD, KT) == True:
                        tt = Thu3(ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung, id_tuan=tuan)
                        tt.save()
                    else:
                        info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'
                else:
                    info = "Thời gian này đã được sử dụng!"
            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    print('Dang chay addt3')
    return render(request, 'admin_add.html', {'id_tuan':id, 'thu':'t3', 'info':info})


def addt4(request, id):
    info = ''
    tuan = Tuan.objects.get(id=id)
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']

        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if max_date_update('thu4', BD, KT) == True:
                    if check_timedelta(BD, KT) == True:
                        tt = Thu4(ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung, id_tuan=tuan)
                        tt.save()
                    else:
                        info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'
                else:
                    info = "Thời gian này đã được sử dụng!"
            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    print('Dang chay addt4')
    return render(request, 'admin_add.html', {'id_tuan':id, 'thu':'t4', 'info':info})

def addt5(request, id):
    info = ''
    tuan = Tuan.objects.get(id=id)
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']

        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if max_date_update('thu5', BD, KT) == True:
                    if check_timedelta(BD, KT) == True:
                        tt = Thu5(ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung, id_tuan=tuan)
                        tt.save()
                    else:
                        info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'
                else:
                    info = "Thời gian này đã được sử dụng!"
            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    print('Dang chay addt5')
    return render(request, 'admin_add.html', {'id_tuan':id, 'thu':'t5', 'info':info})

def addt6(request, id):
    info = ''
    tuan = Tuan.objects.get(id=id)
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if max_date_update('thu6', BD, KT) == True:
                    if check_timedelta(BD, KT) == True:
                        tt = Thu6(ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung, id_tuan=tuan)
                        tt.save()
                    else:
                        info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'
                else:
                    info = "Thời gian này đã được sử dụng!"
            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    print('Dang chay addt6')
    return render(request, 'admin_add.html', {'id_tuan':id, 'thu':'t6', 'info':info})

def addt7(request, id):
    info = ''
    tuan = Tuan.objects.get(id=id)
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']

        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if max_date_update('thu7', BD, KT) == True:
                    if check_timedelta(BD, KT) == True:
                        tt = Thu7(ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung, id_tuan=tuan)
                        tt.save()
                    else:
                        info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'
                else:
                    info = "Thời gian này đã được sử dụng!"
            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    print('Dang chay addt7')
    return render(request, 'admin_add.html', {'id_tuan':id, 'thu':'t7', 'info':info})

def addcn(request, id):
    info = ''
    tuan = Tuan.objects.get(id=id)
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']

        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if max_date_update('chunhat', BD, KT) == True:
                    if check_timedelta(BD, KT) == True:
                        tt = ChuNhat(ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung, id_tuan=tuan)
                        tt.save()
                    else:
                        info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'
                else:
                    info = "Thời gian này đã được sử dụng!"
            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    print('Dang chay addcn')
    return render(request, 'admin_add.html', {'id_tuan':id, 'thu':'cn', 'info':info})


def updatet3(request, id):
    info = ''
    t3 = Thu3.objects.get(id=id)
    # lay id tuan tu bang thu3
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        print('Tieu de la' + TieuDe)
        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if check_timedelta(BD, KT) == True:
                    Thu3.objects.get(id=id).delete()
                    if max_date_update('thu3', BD, KT) == True:
                        tt = Thu3(id=id, ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung,
                                  id_tuan=t3.id_tuan)
                        tt.save()
                    else:
                        tt1 = Thu3(id=id, ThoiGianBD=t3.ThoiGianBD, ThoiGianKT=t3.ThoiGianKT, TieuDe=t3.TieuDe, NoiDung=t3.NoiDung,
                                   id_tuan=t3.id_tuan)
                        tt1.save()
                        info = "Bạn chưa cập nhật thời gian thành công do thời gian này đã được sử dụng!"
                else:
                    info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'

            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"


    return render(request, 'admin_update.html', {'thu': t3, 'day':'t3', 'info':info})

def updatet4(request, id):
    info = ''
    t4 = Thu4.objects.get(id=id)
    # lay id tuan tu bang thu4
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        print('Tieu de la' + TieuDe)
        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if check_timedelta(BD, KT) == True:
                    Thu4.objects.get(id=id).delete()
                    if max_date_update('thu4', BD, KT) == True:
                        tt = Thu4(id=id, ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung,
                                  id_tuan=t4.id_tuan)
                        tt.save()
                    else:
                        tt1 = Thu4(id=id, ThoiGianBD=t4.ThoiGianBD, ThoiGianKT=t4.ThoiGianKT, TieuDe=t4.TieuDe, NoiDung=t4.NoiDung,
                                   id_tuan=t4.id_tuan)
                        tt1.save()
                        info = "Bạn chưa cập nhật thời gian thành công do thời gian này đã được sử dụng!"
                else:
                    info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'

            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    return render(request, 'admin_update.html', {'thu': t4, 'day': 't4', 'info':info})

def updatet5(request, id):
    info = ''
    t5 = Thu5.objects.get(id=id)
    # lay id tuan tu bang thu5
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        print('Tieu de la' + TieuDe)

        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if check_timedelta(BD, KT) == True:
                    Thu5.objects.get(id=id).delete()
                    if max_date_update('thu5', BD, KT) == True:
                        tt = Thu5(id=id, ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung,
                                  id_tuan=t5.id_tuan)
                        tt.save()
                    else:
                        tt1 = Thu5(id=id, ThoiGianBD=t5.ThoiGianBD, ThoiGianKT=t5.ThoiGianKT, TieuDe=t5.TieuDe, NoiDung=t5.NoiDung,
                                   id_tuan=t5.id_tuan)
                        tt1.save()
                        info = "Bạn chưa cập nhật thời gian thành công do thời gian này đã được sử dụng!"
                else:
                    info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'

            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    return render(request, 'admin_update.html', {'thu': t5, 'day': 't5', 'info':info})

def updatet6(request, id):
    info = ''
    t6 = Thu6.objects.get(id=id)
    # lay id tuan tu bang thu5
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        print('Tieu de la' + TieuDe)
        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if check_timedelta(BD, KT) == True:
                    Thu6.objects.get(id=id).delete()
                    if max_date_update('thu6', BD, KT) == True:
                        tt = Thu6(id=id, ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung,
                                  id_tuan=t6.id_tuan)
                        tt.save()
                    else:
                        tt1 = Thu6(id=id, ThoiGianBD=t6.ThoiGianBD, ThoiGianKT=t6.ThoiGianKT, TieuDe=t6.TieuDe, NoiDung=t6.NoiDung,
                                   id_tuan=t6.id_tuan)
                        tt1.save()
                        info = "Bạn chưa cập nhật thời gian thành công do thời gian này đã được sử dụng!"
                else:
                    info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'

            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    return render(request, 'admin_update.html', {'thu': t6, 'day': 't6', 'info':info})

def updatet7(request, id):
    info = ''
    t7 = Thu7.objects.get(id=id)
    # lay id tuan tu bang thu5
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        print('Tieu de la' + TieuDe)

        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if check_timedelta(BD, KT) == True:
                    Thu7.objects.get(id=id).delete()
                    if max_date_update('thu7', BD, KT) == True:
                        tt = Thu7(id=id, ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung,
                                  id_tuan=t7.id_tuan)
                        tt.save()
                    else:
                        tt1 = Thu7(id=id, ThoiGianBD=t7.ThoiGianBD, ThoiGianKT=t7.ThoiGianKT, TieuDe=t7.TieuDe, NoiDung=t7.NoiDung,
                                   id_tuan=t7.id_tuan)
                        tt1.save()
                        info = "Bạn chưa cập nhật thành công do thời gian này đã được sử dụng!"
                else:
                    info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'

            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    return render(request, 'admin_update.html', {'thu': t7, 'day': 't7', 'info':info})

def updatecn(request, id):
    info = ''
    cn = ChuNhat.objects.get(id=id)
    # lay id tuan tu bang thu5
    if request.method == 'POST':
        BD = request.POST['BD']
        KT = request.POST['KT']
        TieuDe = request.POST['TieuDe']
        NoiDung = request.POST['NoiDung']
        print('Tieu de la' + TieuDe)

        if check_6h_17h30(BD, KT) == True:
            if check_empty(TieuDe) == True:
                if check_timedelta(BD, KT) == True:
                    ChuNhat.objects.get(id=id).delete()
                    if max_date_update('chunhat', BD, KT) == True:
                        tt = ChuNhat(id=id, ThoiGianBD=BD, ThoiGianKT=KT, TieuDe=TieuDe, NoiDung=NoiDung,
                                  id_tuan=cn.id_tuan)
                        tt.save()
                    else:
                        tt1 = ChuNhat(id=id, ThoiGianBD=cn.ThoiGianBD, ThoiGianKT=cn.ThoiGianKT, TieuDe=cn.TieuDe, NoiDung=cn.NoiDung,
                                   id_tuan=cn.id_tuan)
                        tt1.save()
                        info = "Bạn chưa cập nhật thời gian thành công do thời gian này đã được sử dụng!"
                else:
                    info = 'Thời gian kết thúc phải lớn hơn thời gian bắt đầu'

            else:
                info = "Vui lòng nhập tiêu đề!"
        else:
            info = "Thời gian bắt đầu sớm nhất là 6h00 và kết thúc lúc 17h30!"
    return render(request, 'admin_update.html', {'thu': cn, 'day': 'cn', 'info':info})

def deletet2(request, id):
    try:
        Thu2.objects.get(id=id)
        field_name = 'id_tuan'
        field_object = Thu2._meta.get_field(field_name)
        obj = Thu2.objects.first()
        id_tuan = field_object.value_from_object(obj)
        Thu2.objects.get(id=id).delete()
        print("id tuan la: " + str(id_tuan))
        id1 = Tuan.objects.get(id=id_tuan)
        showt2 = Thu2.objects.filter(id_tuan=id1)
        showt3 = Thu3.objects.filter(id_tuan=id1)
        showt4 = Thu4.objects.filter(id_tuan=id1)
        showt5 = Thu5.objects.filter(id_tuan=id1)
        showt6 = Thu6.objects.filter(id_tuan=id1)
        showt7 = Thu7.objects.filter(id_tuan=id1)
        showcn = ChuNhat.objects.filter(id_tuan=id1)
        return render(request, 'admin_chonngay.html', {'showt2': showt2, 'showt3': showt3,
                                                       'showt4': showt4, 'showt5': showt5, 'showt6': showt6,
                                                       'showt7': showt7,
                                                       'showcn': showcn, 'Time': id1.NgayBD, 'id_tuan': id_tuan})
    except Thu2.DoesNotExist:
        return redirect('../')

def deletet3(request,id):
    try:
        Thu3.objects.get(id=id)
        field_name = 'id_tuan'
        field_object = Thu3._meta.get_field(field_name)
        obj = Thu3.objects.first()
        id_tuan = field_object.value_from_object(obj)
        Thu3.objects.get(id=id).delete()
        print("id tuan la: " + str(id_tuan))
        id1 = Tuan.objects.get(id=id_tuan)
        showt2 = Thu2.objects.filter(id_tuan=id1)
        showt3 = Thu3.objects.filter(id_tuan=id1)
        showt4 = Thu4.objects.filter(id_tuan=id1)
        showt5 = Thu5.objects.filter(id_tuan=id1)
        showt6 = Thu6.objects.filter(id_tuan=id1)
        showt7 = Thu7.objects.filter(id_tuan=id1)
        showcn = ChuNhat.objects.filter(id_tuan=id1)
        return render(request, 'admin_chonngay.html', {'showt2': showt2, 'showt3': showt3,
                                                       'showt4': showt4, 'showt5': showt5, 'showt6': showt6,
                                                       'showt7': showt7,
                                                       'showcn': showcn, 'Time': id1.NgayBD, 'id_tuan': id_tuan})
    except Thu3.DoesNotExist:
        return redirect('../')

def deletet4(request,id):
    try:
        Thu4.objects.get(id=id)
        field_name = 'id_tuan'
        field_object = Thu4._meta.get_field(field_name)
        obj = Thu4.objects.first()
        id_tuan = field_object.value_from_object(obj)
        Thu4.objects.get(id=id).delete()
        print("id tuan la: " + str(id_tuan))
        id1 = Tuan.objects.get(id=id_tuan)
        showt2 = Thu2.objects.filter(id_tuan=id1)
        showt3 = Thu3.objects.filter(id_tuan=id1)
        showt4 = Thu4.objects.filter(id_tuan=id1)
        showt5 = Thu5.objects.filter(id_tuan=id1)
        showt6 = Thu6.objects.filter(id_tuan=id1)
        showt7 = Thu7.objects.filter(id_tuan=id1)
        showcn = ChuNhat.objects.filter(id_tuan=id1)
        return render(request, 'admin_chonngay.html', {'showt2': showt2, 'showt3': showt3,
                                                       'showt4': showt4, 'showt5': showt5, 'showt6': showt6,
                                                       'showt7': showt7,
                                                       'showcn': showcn, 'Time': id1.NgayBD, 'id_tuan': id_tuan})
    except Thu4.DoesNotExist:
        return redirect('../')



def deletet5(request,id):
    try:
        Thu5.objects.get(id=id)
        field_name = 'id_tuan'
        field_object = Thu5._meta.get_field(field_name)
        obj = Thu5.objects.first()
        id_tuan = field_object.value_from_object(obj)
        Thu5.objects.get(id=id).delete()
        print("id tuan la: " + str(id_tuan))
        id1 = Tuan.objects.get(id=id_tuan)
        showt2 = Thu2.objects.filter(id_tuan=id1)
        showt3 = Thu3.objects.filter(id_tuan=id1)
        showt4 = Thu4.objects.filter(id_tuan=id1)
        showt5 = Thu5.objects.filter(id_tuan=id1)
        showt6 = Thu6.objects.filter(id_tuan=id1)
        showt7 = Thu7.objects.filter(id_tuan=id1)
        showcn = ChuNhat.objects.filter(id_tuan=id1)
        return render(request, 'admin_chonngay.html', {'showt2': showt2, 'showt3': showt3,
                                                       'showt4': showt4, 'showt5': showt5, 'showt6': showt6,
                                                       'showt7': showt7,
                                                       'showcn': showcn, 'Time': id1.NgayBD, 'id_tuan': id_tuan})
    except Thu5.DoesNotExist:
        return redirect('../')

def deletet6(request,id):
    try:
        Thu6.objects.get(id=id)
        field_name = 'id_tuan'
        field_object = Thu6._meta.get_field(field_name)
        obj = Thu6.objects.first()
        id_tuan = field_object.value_from_object(obj)
        Thu6.objects.get(id=id).delete()
        print("id tuan la: " + str(id_tuan))
        id1 = Tuan.objects.get(id=id_tuan)
        showt2 = Thu2.objects.filter(id_tuan=id1)
        showt3 = Thu3.objects.filter(id_tuan=id1)
        showt4 = Thu4.objects.filter(id_tuan=id1)
        showt5 = Thu5.objects.filter(id_tuan=id1)
        showt6 = Thu6.objects.filter(id_tuan=id1)
        showt7 = Thu7.objects.filter(id_tuan=id1)
        showcn = ChuNhat.objects.filter(id_tuan=id1)
        return render(request, 'admin_chonngay.html', {'showt2': showt2, 'showt3': showt3,
                                                       'showt4': showt4, 'showt5': showt5, 'showt6': showt6,
                                                       'showt7': showt7,
                                                       'showcn': showcn, 'Time': id1.NgayBD, 'id_tuan': id_tuan})
    except Thu6.DoesNotExist:
        return redirect('../')


def deletet7(request,id):
    try:
        Thu7.objects.get(id=id)
        field_name = 'id_tuan'
        field_object = Thu7._meta.get_field(field_name)
        obj = Thu7.objects.first()
        id_tuan = field_object.value_from_object(obj)
        Thu7.objects.get(id=id).delete()
        print("id tuan la: " + str(id_tuan))
        id1 = Tuan.objects.get(id=id_tuan)
        showt2 = Thu2.objects.filter(id_tuan=id1)
        showt3 = Thu3.objects.filter(id_tuan=id1)
        showt4 = Thu4.objects.filter(id_tuan=id1)
        showt5 = Thu5.objects.filter(id_tuan=id1)
        showt6 = Thu6.objects.filter(id_tuan=id1)
        showt7 = Thu7.objects.filter(id_tuan=id1)
        showcn = ChuNhat.objects.filter(id_tuan=id1)
        return render(request, 'admin_chonngay.html', {'showt2': showt2, 'showt3': showt3,
                                                       'showt4': showt4, 'showt5': showt5, 'showt6': showt6,
                                                       'showt7': showt7,
                                                       'showcn': showcn, 'Time': id1.NgayBD, 'id_tuan': id_tuan})
    except Thu7.DoesNotExist:
        return redirect('../')


def deletecn(request,id):
    try:
        ChuNhat.objects.get(id=id)
        field_name = 'id_tuan'
        field_object = ChuNhat._meta.get_field(field_name)
        obj = ChuNhat.objects.first()
        id_tuan = field_object.value_from_object(obj)
        ChuNhat.objects.get(id=id).delete()
        print("id tuan la: " + str(id_tuan))
        id1 = Tuan.objects.get(id=id_tuan)
        showt2 = Thu2.objects.filter(id_tuan=id1)
        showt3 = Thu3.objects.filter(id_tuan=id1)
        showt4 = Thu4.objects.filter(id_tuan=id1)
        showt5 = Thu5.objects.filter(id_tuan=id1)
        showt6 = Thu6.objects.filter(id_tuan=id1)
        showt7 = Thu7.objects.filter(id_tuan=id1)
        showcn = ChuNhat.objects.filter(id_tuan=id1)
        return render(request, 'admin_chonngay.html', {'showt2': showt2, 'showt3': showt3,
                                                       'showt4': showt4, 'showt5': showt5, 'showt6': showt6,
                                                       'showt7': showt7,
                                                       'showcn': showcn, 'Time': id1.NgayBD, 'id_tuan': id_tuan})
    except ChuNhat.DoesNotExist:
        return redirect('../')




def chonngay(request, id):
    TK = TaiKhoan.objects.all()
    if (tmp.tk == TK[0].usr) and (tmp.mk == TK[0].pwd):
        id1 = Tuan.objects.filter(id=id)
        for x in id1:
            id_show = x.id
            NgayBD = x.NgayBD
        showt2 = Thu2.objects.filter(id_tuan=id_show)
        showt3 = Thu3.objects.filter(id_tuan=id_show)
        showt4 = Thu4.objects.filter(id_tuan=id_show)
        showt5 = Thu5.objects.filter(id_tuan=id_show)
        showt6 = Thu6.objects.filter(id_tuan=id_show)
        showt7 = Thu7.objects.filter(id_tuan=id_show)
        showcn = ChuNhat.objects.filter(id_tuan=id_show)
        return render(request, 'admin_chonngay.html', {'showt2': showt2, 'showt3': showt3,
                                                       'showt4': showt4, 'showt5': showt5, 'showt6': showt6,
                                                       'showt7': showt7,
                                                       'showcn': showcn, 'Time': NgayBD, 'id_tuan': id})
    else:
        return redirect('../../login')


def sendmail(request):
    if request.method=='POST':
        usr = TaiKhoan.objects.get(id=1)
        mail_usr = usr.mail
        mail = request.POST['mail']
        message = '''Bạn nhận được yêu cầu cấp mật khẩu xem lịch từ tài khoản {}

                    '''.format(mail)
        email = EmailMessage(
            'BLOG: Yêu cầu cấp mật khẩu',
            message,
            '',
            ['django.projects.test@gmail.com'],
            # reply_to=['v1t223334444@gmail.com'],
            cc=[mail_usr],
        )
        email.send(fail_silently=False)
        return render(request, 'info.html', {'info': 'Bạn vừa gửi thành công yêu cầu cấp mật khẩu cho tài khoản ' + mail +'!'})
        # mail = request.POST['mail']
        # message = '''Bạn nhận được yêu cầu cấp mật khẩu xem lịch từ tài khoản {}
        #
        #     '''.format(mail)
        # send_mail('BLOG: Yêu cầu cấp mật khẩu', message, '', ['nguyen01vy12@gmail.com'], fail_silently=False)

    return render(request, 'info.html', {'info': 'Thao tác thất bại!'})

def check_empty(TieuDe):
    if TieuDe =="":
        return False
    else:
        return True

def check_timedelta(BD, KT):
    dt = "2021-01-01 " + BD
    day = datetime.strptime(dt, "%Y-%m-%d %H:%M")
    hour = day.hour
    min = day.minute
    second = day.second

    dt1 = "2021-01-01 " + KT
    day1 = datetime.strptime(dt1, "%Y-%m-%d %H:%M")
    hour1 = day1.hour
    min1 = day1.minute
    second1 = day1.second
    # time1 = day1.time()
    delta1 = timedelta(hours=hour1, minutes=min1, seconds=second1)
    delta = timedelta(hours=hour, minutes=min, seconds=second)
    kq = delta1 - delta
    if kq > timedelta(hours=0, minutes=0, seconds=0):
      return True
    else:
      return False


# def max_time(sql, TG_BD):
#     cursor = connection.cursor()
#     cursor.execute(sql)
#
#     dateBD = "2021-01-01 "+TG_BD
#     day = datetime.strptime(dateBD, "%Y-%m-%d %H:%M")
#     BD_h = day.hour
#     BD_m = day.minute
#     BD_s = day.second
#
#     max_date = cursor.fetchone()[0]
#     if max_date == None:
#         return True
#     else:
#         max_date_h = max_date.hour
#         max_date_m = max_date.minute
#         max_date_s = max_date.second
#
#         delta1 = timedelta(hours=BD_h, minutes=BD_m, seconds=BD_s)
#         delta = timedelta(hours=max_date_h, minutes=max_date_m, seconds=max_date_s)
#         kq = delta1 - delta
#         if kq < timedelta(hours=0, minutes=0, seconds=0):
#             return False
#         else:
#             return True

def check_6h_17h30(BD, KT):
    dateBD = "2021-01-01 " + BD
    dateKT = "2021-01-01 " + KT

    dayBD = datetime.strptime(dateBD, "%Y-%m-%d %H:%M")
    BD_h = dayBD.hour
    BD_m = dayBD.minute
    BD_s = dayBD.second

    dayKT = datetime.strptime(dateKT, "%Y-%m-%d %H:%M")
    KT_h = dayKT.hour
    KT_m = dayKT.minute
    KT_s = dayKT.second

    if timedelta(hours=BD_h, minutes=BD_m, seconds=BD_s) < timedelta(hours=6, minutes=0, seconds=0) or \
            timedelta(hours=KT_h, minutes=KT_m, seconds=KT_s) > timedelta(hours=17, minutes=30, seconds=0):
        return False
    else:
        return True


def max_date_update(thu, BD1, KT1):
    sql = "SELECT COUNT(*) FROM `lichlamviec_"+thu+"` WHERE '"+BD1+"' <= ThoiGianBD and (ThoiGianBD < '"+KT1+"' or ThoiGianBD = '"+KT1+"') "
    sql1 = "SELECT COUNT(*) FROM `lichlamviec_"+thu+"` WHERE ThoiGianBD <= '"+BD1+"'and '"+BD1+"' <= ThoiGianKT"
    cursor = connection.cursor()
    cursor.execute(sql)
    cantrai = cursor.fetchone()[0]

    cursor.execute(sql1)
    canphai = cursor.fetchone()[0]

    if cantrai != 0:
        return False
    elif canphai != 0:
        return False
    else:
        return True
