from django.contrib import admin
from .models import calendario

class calendarioAdmin(admin.ModelAdmin):
    list_display = ('titulo','descricao','data_inicial','data_final')

admin.site.register(calendario,calendarioAdmin)