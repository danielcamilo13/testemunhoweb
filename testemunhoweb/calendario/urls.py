from django.urls import path
from . import views
from .views import EventFeed


urlpatterns = [
    path('',views.index,name='index'),
    path('feed/feed.ics',EventFeed()),
    # path('feed/',views.index,name='index'),
]