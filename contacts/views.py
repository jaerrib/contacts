import csv

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
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


class SearchResultsView(ListView):
    model = Contact
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("search")
        object_list = Contact.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(email__icontains=query)
        )
        return object_list


def export_contact_list(request):
    query_set = Contact.objects.filter(creator=request.user.pk).order_by(
        "last_name", "first_name"
    )
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="exported_contacts.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["First Name", "Last Name", "Phone Number", "Email"])
    for item in query_set:
        writer.writerow(
            [item.last_name, item.first_name, item.phone_number, item.email]
        )
    return response
