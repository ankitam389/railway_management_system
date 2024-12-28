from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('train/add/', views.add_train),
    path('availability/<str:source>/<str:destination>/', views.get_seat_availability),
    path('book/<int:train_id>/', views.book_seat),
    path('booking/<int:booking_id>/', views.get_booking_details),
]
