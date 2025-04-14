from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('Crop-disease/',views.disease,name='disease'),
    path('Crop-disease-prediction/',views.disease_prediction,name='disease_prediction'),
    path('contact/', views.contact, name='contact'),
    path('predict/', views.image_prediction, name='image_prediction'),
    path('ajax-predict/', views.ajax_predict, name='ajax_predict'),
]
