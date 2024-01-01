from django.views.generic import ListView, DetailView

from .models import Contact


class ContactListView(ListView):
    model = Contact
    template_name = "contact_list.html"


class ContactDetailView(DetailView):
    model = Contact
    template_name = "contact_detail.html"
