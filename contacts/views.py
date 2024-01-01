from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Contact


class ContactListView(ListView):
    model = Contact
    template_name = "contact_list.html"


class ContactDetailView(DetailView):
    model = Contact
    template_name = "contact_detail.html"


class ContactCreateView(CreateView):
    model = Contact
    template_name = "create_new.html"
    fields = ["first_name", "last_name", "phone_number", "email", "creator"]


class ContactUpdateView(UpdateView):
    model = Contact
    template_name = "contact_edit.html"
    fields = ["first_name", "last_name", "phone_number", "email"]


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contact_delete.html"
    success_url = reverse_lazy("contact_list")
