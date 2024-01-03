from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Contact


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contact_list.html"
    ordering = ["last_name", "first_name"]


class ContactDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Contact
    template_name = "contact_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = "create_new.html"
    fields = ("first_name", "last_name", "phone_number", "email")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Contact
    fields = ["first_name", "last_name", "phone_number", "email"]
    template_name = "contact_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user


class ContactDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Contact
    template_name = "contact_delete.html"
    success_url = reverse_lazy("contact_list")

    def test_func(self):
        obj = self.get_object()
        return obj.creator == self.request.user
