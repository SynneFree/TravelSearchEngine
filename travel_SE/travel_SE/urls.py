"""travel_SE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    url(r'^home$', views.index),
    # url(r'^get_city$', views.get_city,name='get_city'),
    # url(r'^get_area$', views.get_area,name='get_area'),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^collect$', views.collect),
    url(r'^check-collect$', views.check_collect),
    url(r'^cancel-collect$', views.cancel_collect),

    url(r'^check-history$', views.check_history),
    url(r'^personal-center$', views.personal_center),

    url(r'^check-hot$', views.check_hot),
    url(r'^check-all$', views.check_all),


    url(r'^register$', views.register,name='register'),
    url(r'^search$', views.search),
    url(r'^search-by-area$', views.search_by_area),
    url(r'^attraction-detail$', views.attraction_detail),
    url(r'^publish-comment$', views.publish_comment),
    url(r'^load-comment$', views.load_comment),

    url(r'^page-test$', views.page_test),

    url(r'^test-add$', views.test_add),
    #url(r'^search-by-city$', views.search_by_city),
    #url(r'^search-(?P<area>\d+)$', views.search_by_area),
]
