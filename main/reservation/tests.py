from django.test import TestCase
from django.urls import reverse
from .models import User, OfferType, Offer, Ticket, Cart, Transaction
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

# Tests pour le modèle User
class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', phone_number='1234567890', address='123 Street Name')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertEqual(self.user.address, '123 Street Name')
        self.assertFalse(self.user.is_verified)

    def test_user_verification(self):
        self.user.is_verified = True
        self.user.save()
        self.assertTrue(self.user.is_verified)

# Tests pour le modèle OfferType
class OfferTypeModelTest(TestCase):

    def setUp(self):
        self.offer_type = OfferType.objects.create(name='VIP')

    def test_offer_type_creation(self):
        self.assertEqual(self.offer_type.name, 'VIP')

# Tests pour le modèle Offer
class OfferModelTest(TestCase):

    def setUp(self):
        self.offer_type = OfferType.objects.create(name='Standard')
        self.offer = Offer.objects.create(
            offer_type=self.offer_type,
            description='Standard ticket',
            price=50.0,
            availability=100,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            image=''  # Assurez-vous que l'image est une chaîne vide
        )

    def test_offer_creation(self):
        self.assertEqual(self.offer.description, 'Standard ticket')
        self.assertEqual(self.offer.price, 50.0)
        self.assertEqual(self.offer.availability, 100)
        self.assertEqual(self.offer.image.name, '')  # Vérifiez si l'image est une chaîne vide

# Tests pour le modèle Ticket
class TicketModelTest(TestCase):

    def setUp(self):
        self.offer_type = OfferType.objects.create(name='Standard')
        self.offer = Offer.objects.create(
            offer_type=self.offer_type,
            description='Standard ticket',
            price=50.0,
            availability=100,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )
        self.ticket = Ticket.objects.create(offer=self.offer, ticket_key='ABC123')

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.ticket_key, 'ABC123')
        self.assertTrue(self.ticket.is_valid)

# Tests pour le modèle Cart
class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.offer_type = OfferType.objects.create(name='Standard')
        self.offer = Offer.objects.create(
            offer_type=self.offer_type,
            description='Standard ticket',
            price=50.0,
            availability=100,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )
        self.ticket = Ticket.objects.create(offer=self.offer, ticket_key='ABC123')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user.username, 'testuser')
        self.cart.tickets.add(self.ticket)
        self.assertEqual(self.cart.tickets.count(), 1)

# Tests pour le modèle Transaction
class TransactionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.offer_type = OfferType.objects.create(name='Standard')
        self.offer = Offer.objects.create(
            offer_type=self.offer_type,
            description='Standard ticket',
            price=50.0,
            availability=100,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )
        self.ticket = Ticket.objects.create(offer=self.offer, ticket_key='ABC123')
        self.transaction = Transaction.objects.create(user=self.user, total_amount=50.0)
        self.transaction.tickets.add(self.ticket)

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.user.username, 'testuser')
        self.assertEqual(self.transaction.total_amount, 50.0)
        self.assertEqual(self.transaction.tickets.count(), 1)

# Tests pour les vues
class ViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_authenticated_user_access(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')

# Tests pour le formulaire CustomUserCreationForm
from .forms import CustomUserCreationForm

class CustomUserCreationFormTest(TestCase):

    def test_custom_user_creation_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

# Tests pour vérifier les accès protégés
class ProtectedViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_protected_view_redirects(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)  # Utiliser assertIn pour vérifier l'URL de redirection

    def test_protected_view_access(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')


# Tests pour l'ajout au panier
class AddToCartTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.offer_type = OfferType.objects.create(name='Standard')
        self.offer = Offer.objects.create(
            offer_type=self.offer_type,
            description='Standard ticket',
            price=50.0,
            availability=100,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )

    def test_add_to_cart_authenticated_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_to_cart', args=[self.offer.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'cart_count': 1})
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.tickets.count(), 1)
