from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import Offer, Cart, Ticket, Transaction
import uuid
from django.conf import settings
from django.db import transaction as db_transaction
import requests
import qrcode
from io import BytesIO
import logging
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
logger = logging.getLogger(__name__)



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



@login_required
def account(request):
    editing = False  

    if 'edit' in request.GET:
        editing = True

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'account.html', {'form': form, 'editing': editing})

def list_offers(request):
    offers = Offer.objects.all()  # Récupère toutes les offres
    return render(request, 'list_offers.html', {'offers': offers})


def view_cart(request):
    context = {}
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        context['tickets'] = cart.tickets.all()
        context['total_amount'] = calculate_total_amount(context['tickets'])
    else:
        offer_ids = request.session.get('cart', [])
        offers = Offer.objects.filter(id__in=offer_ids)
        context['offers'] = offers
        context['total_amount'] = sum(offer.price for offer in offers)

    return render(request, 'view_cart.html', context)

def add_to_cart(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        unique_ticket_key = str(uuid.uuid4())  
        ticket = Ticket.objects.create(offer=offer, ticket_key=unique_ticket_key)
        cart.tickets.add(ticket)
    else:
        cart = request.session.get('cart', [])
        cart.append(offer_id)
        request.session['cart'] = cart

    return redirect('list_offers')

@login_required
def update_cart(request, ticket_id, quantity):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            try:
                ticket = cart.tickets.get(id=ticket_id)
                ticket.quantity = quantity
                ticket.save()
            except Ticket.DoesNotExist:
                pass
        else:
            pass

        return redirect('view_cart')
    else:
        return redirect('home')


def generate_qr_code(final_key):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(final_key)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return File(buffer, name=f"{final_key}.png")

@login_required
def finalize_purchase(request):
    logger.info("Debug: Entering my_function")
    cart, created = Cart.objects.get_or_create(user=request.user)
    if not cart.tickets.exists():
        logger.info("Tentative de finalisation d'achat avec un panier vide.")
        return render(request, 'error.html', {'message': 'Votre panier est vide.'})

    try:
        with transaction.atomic():
            for ticket in cart.tickets.all():
                offer = Offer.objects.select_for_update().get(id=ticket.offer.id)
                logger.info(f"Avant décrémentation - Offer ID: {offer.id}, Availability: {offer.availability}")
                if offer.availability > 0:
                    offer.availability -= 1
                    offer.save()
                    logger.info(f"Après décrémentation - Offer ID: {offer.id}, Availability: {offer.availability}")
                else:
                    logger.info(f"Offre non disponible - Offer ID: {offer.id}")
                    return render(request, 'error.html', {'message': "L'offre n'est plus disponible."})
            
            total_amount = calculate_total_amount(cart.tickets.all())
            transaction = Transaction.objects.create(
                user=request.user,
                total_amount=total_amount,
                payment_method="Mock Payment",
                transaction_status="Completed"
            )
            for ticket in cart.tickets.all():
                transaction.tickets.add(ticket)
            cart.tickets.clear()
            return redirect('payment_confirmation')
    except Exception as e:
        logger.info("Exception lors de la finalisation de l'achat.")
        logger.info("Debug: Exiting my_function")
        return render(request, 'error.html', {'message': str(e)})

    return render(request, 'purchase_confirmation.html')

def calculate_total_amount(tickets):
    return sum(ticket.offer.price for ticket in tickets)

@login_required
def payment_confirmation(request):
    return render(request, 'payment_confirmation.html')

@login_required
def process_payment(request):
    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        total_amount = calculate_total_amount(cart.tickets.all())

        transaction = Transaction.objects.create(
            user=request.user,
            total_amount=total_amount,
            payment_method="Mock Payment",
            transaction_status="Completed"
        )

        for ticket in cart.tickets.all():
            ticket.purchase_key = str(uuid.uuid4())
            final_key = f"{str(request.user.user_key)}-{ticket.purchase_key}"
            qr_code_file = generate_qr_code(final_key)
            ticket.qr_code.save(f"{final_key}.png", qr_code_file, save=True)
            ticket.save()

            transaction.tickets.add(ticket)

        cart.tickets.clear()
        return redirect('payment_confirmation')

    return redirect('checkout')


def checkout(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        tickets = cart.tickets.all()
        total_amount = calculate_total_amount(tickets)

        return render(request, 'checkout.html', {'total_amount': total_amount})
    else:
        return redirect('login')
    

def remove_from_cart(request, ticket_id):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            ticket = Ticket.objects.get(id=ticket_id, cart=cart)
            cart.tickets.remove(ticket)
        except Ticket.DoesNotExist:
            pass
    else:
        cart = request.session.get('cart', [])
        if ticket_id in cart:
            cart.remove(ticket_id)
            request.session['cart'] = cart

    return redirect('view_cart')

    

@login_required
def my_orders(request):
    transactions = Transaction.objects.filter(user=request.user).prefetch_related('tickets')
    return render(request, 'my_orders.html', {'transactions': transactions})

@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})