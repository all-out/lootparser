from django.contrib import admin
from main.models import Paste, Op, Character, Tax, Participation


class PasteAdmin(admin.ModelAdmin):
    list_display = [
        'ep_id',
        'created',
        'op',
        'blueloot_value',
        'salvage_value',
        'total_value',
        'ep_totals_volume',
        'tax',
    ]


admin.site.register(Paste, PasteAdmin)
admin.site.register(Character)
admin.site.register(Op)
admin.site.register(Tax)
admin.site.register(Participation)
