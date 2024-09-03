from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Contact


class ContactHistoryAdmin(SimpleHistoryAdmin):
    list_display = [
        "last_name",
        "first_name",
        "phone_number",
        "email",
        "creator",
    ]
    search_fields = [
        "last_name",
        "first_name",
        "phone_number",
        "email",
    ]


admin.site.register(Contact, ContactHistoryAdmin)
