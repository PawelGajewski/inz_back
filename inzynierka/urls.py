from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from warsztat import views

from warsztat.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('addcar/', AddCarView.as_view()),
    path('user/<int:pk>/', UserViewPK.as_view()),
    path('users/', UserListView.as_view()),
    path('car/<int:pk>/', CarViewPK.as_view()),
    path('carlist/<int:pk>/', CarListView.as_view()),
    path('service/<int:pk>/', ServiceViewPK.as_view()),
    path('servicelist/<int:pk>/', ServiceListView.as_view()),
    path('servicelistpresent/<int:pk>/', ServiceListViewPresent.as_view()),
    path('service/', ServiceListView.as_view()),
    path('email/<int:pk>/', Email.as_view()),
    path('emailaccept/<int:pk>/', EmailAccept.as_view()),
    path('addpart/', Addpart.as_view()),
    path('getparts/<int:pk>/', Getparts.as_view()),
    path('reservation/', AdminServiceReservation.as_view()),
    path('history/', AdminServiceFinishedView.as_view()),
    path('inprogress/', AdminServiceInProgress.as_view())
]
