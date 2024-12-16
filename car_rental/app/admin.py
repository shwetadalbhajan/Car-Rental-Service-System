from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Car)
admin.site.register(ContactSubmission)
admin.site.register(Wishlist)
admin.site.register(Booking)
admin.site.register(BookingHistory)