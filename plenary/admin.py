from django.contrib import admin
from plenary.models import Pleniere, AgendaItem, Deputy, Party

admin.site.register(Pleniere)
admin.site.register(AgendaItem)
admin.site.register(Deputy)
admin.site.register(Party)
