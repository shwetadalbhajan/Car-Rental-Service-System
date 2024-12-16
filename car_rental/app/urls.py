from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.landing_page_view, name='landing'),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
    path("contact/", views.contact, name="contact"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('reset_password_otp/', views.reset_password_otp_view, name='reset_password_otp'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('wishlist/add/<int:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:car_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('payment-success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('booking-history/',views.booking_history, name='booking_history'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('profile/', views.user_profile, name='profile'),
    path('verify_email/', views.verify_email, name='verify_email'),
]

