from django.contrib import admin
from .models import Token


class TokenAdmin(admin.ModelAdmin):
    readonly_fields = ('phase', 'contract_address')


admin.site.register(Token, TokenAdmin)
