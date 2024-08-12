from django.contrib import admin

from lendings.models import Lending


@admin.register(Lending)
class LandingAdmin(admin.ModelAdmin):
    list_filter = ('user', 'book', 'lending_date', 'return_date')
   