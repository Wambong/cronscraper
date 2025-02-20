from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
def redirect_to_news(request):
    return redirect('/api/news/')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', redirect_to_news),
    path('api/', include('news.urls')),
]
