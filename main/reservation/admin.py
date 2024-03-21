from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Offer, Ticket, Cart, Transaction, OfferType
from django.utils.safestring import mark_safe


# Admin pour User
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'user_key')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('user_key',)

admin.site.register(User, UserAdmin)

# Admin pour Offer
@admin.register(OfferType)
class OfferTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('get_offer_type', 'price', 'availability', 'start_date', 'end_date', 'image_display')
    list_filter = ('offer_type__name', 'start_date', 'end_date')
    search_fields = ('offer_type__name',)

    def get_offer_type(self, obj):
        return obj.offer_type.name
    get_offer_type.admin_order_field = 'offer_type__name'  
    get_offer_type.short_description = 'Type d\'offre'

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return "No Image"
    image_display.short_description = 'Image'

class TicketAdmin(admin.ModelAdmin):
    list_display = ('offer', 'ticket_key', 'purchase_key', 'qr_code_display', 'is_valid', 'use_date')
    list_filter = ('offer', 'is_valid')
    search_fields = ('ticket_key', 'purchase_key')
    readonly_fields = ('ticket_key', 'purchase_key', 'qr_code')

    def qr_code_display(self, obj):
        if obj.qr_code:
            return mark_safe(f'<img src="{obj.qr_code.url}" width="100" height="100" />')
        return "No QR Code"
    qr_code_display.short_description = 'QR Code'

admin.site.register(Ticket, TicketAdmin)

# Admin pour Cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)

admin.site.register(Cart, CartAdmin)

# Admin pour Transaction
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_date', 'total_amount', 'transaction_status', 'get_tickets')
    list_filter = ('transaction_status', 'transaction_date')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('transaction_date',)

    def get_tickets(self, obj):
        return ", ".join([f"{ticket.offer} - Key: {ticket.ticket_key}" for ticket in obj.tickets.all()])
    get_tickets.short_description = 'Tickets'

admin.site.register(Transaction, TransactionAdmin)

# Configuration du header de l'administration
admin.site.site_header = 'Administration JO 2024 Paris'
admin.site.site_title = 'Site Admin JO 2024 Paris'
admin.site.index_title = 'Gestion des Réservations'
