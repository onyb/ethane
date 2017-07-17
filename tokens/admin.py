from django.contrib import admin
from .models import Token

class TokenAdmin(admin.ModelAdmin):
    pass
admin.site.register(Token, TokenAdmin)
