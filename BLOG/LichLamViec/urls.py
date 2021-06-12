from django.urls import path

from . import views

urlpatterns =  [
    path('', views.homepage),
    path('login', views.showLoginForm),
    path('admin/', views.login),
    path('logout/', views.logout),
    path('sendmail', views.sendmail),
    path('admin/changepass', views.changepass),
    path('admin/changemail', views.changemail),
    path('admin/calendar_pass', views.calendar_pass),
    path('admin/selected/<int:id>', views.chonngay),
    path('admin/update/mon&<int:id>', views.updatet2),
    path('admin/update/tue&<int:id>', views.updatet3),
    path('admin/update/wed&<int:id>', views.updatet4),
    path('admin/update/thur&<int:id>', views.updatet5),
    path('admin/update/fri&<int:id>', views.updatet6),
    path('admin/update/sat&<int:id>', views.updatet7),
    path('admin/update/sun&<int:id>', views.updatecn),
    path('admin/delete/mon&<int:id>', views.deletet2),
    path('admin/delete/tue&<int:id>', views.deletet3),
    path('admin/delete/wed&<int:id>', views.deletet4),
    path('admin/delete/thur&<int:id>', views.deletet5),
    path('admin/delete/fri&<int:id>', views.deletet6),
    path('admin/delete/sat&<int:id>', views.deletet7),
    path('admin/delete/sun&<int:id>', views.deletecn),
    path('admin/selected/add/mon&<int:id>', views.addt2_show),
    path('admin/selected/add/mon2&<int:id>', views.addt2),
    path('admin/selected/add/tue&<int:id>', views.addt3),
    path('admin/selected/add/wed&<int:id>', views.addt4),
    path('admin/selected/add/thur&<int:id>', views.addt5),
    path('admin/selected/add/fri&<int:id>', views.addt6),
    path('admin/selected/add/sat&<int:id>', views.addt7),
    path('admin/selected/add/sun&<int:id>', views.addcn)

]