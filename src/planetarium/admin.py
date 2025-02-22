from django.contrib import admin

from planetarium.models import ShowTheme, Show, Event, TicketType, Ticket, Booking, Dome

admin.site.register(Dome)
admin.site.register(ShowTheme)
admin.site.register(Show)
admin.site.register(Event)
admin.site.register(TicketType)
admin.site.register(Ticket)
admin.site.register(Booking)
