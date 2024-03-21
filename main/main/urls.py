from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views
from reservation.views import register
from reservation import views as reservation_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home_page'),
    path('reservation/', include('reservation.urls')),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/', reservation_views.account, name='account'),
    path('offers/', reservation_views.list_offers, name='list_offers'),
    path('cart/', reservation_views.view_cart, name='view_cart'),
    path('finalize_purchase/', reservation_views.finalize_purchase, name='finalize_purchase'),
    path('process_payment/', reservation_views.process_payment, name='process_payment'),
    path('add-to-cart/<int:offer_id>/', reservation_views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:ticket_id>/', reservation_views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', reservation_views.checkout, name='checkout'),
    path('payment-confirmation/', reservation_views.payment_confirmation, name='payment_confirmation'),
    path('my_orders/', reservation_views.my_orders, name='my_orders'),
    path('update_cart/', reservation_views.update_cart, name='update_cart'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)