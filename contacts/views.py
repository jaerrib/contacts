import csv
import hashlib
import json

import requests
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

    def get_context_data(self, *args, **kwargs):
        obj = self.get_object()
        context = super(ContactDetailView, self).get_context_data(**kwargs)
        context["gravatar_profile"] = deserialize_gravatar_profile(obj.email)
        return context

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


def deserialize_gravatar_profile(email):
    email_encoded = email.lower().encode("utf-8")
    email_hash = hashlib.sha256(email_encoded).hexdigest()
    url = requests.get(f"https://www.gravatar.com/{email_hash}.json")
    if url.status_code != 200:
        return None
    text = url.text
    data = json.loads(text)
    user = data["entry"][0]
    gravatar_profile = {
        "hash": user["hash"],
        "requestHash": user["requestHash"],
        "profileUrl": user["profileUrl"],
        "preferredUsername": user["preferredUsername"],
        "thumbnailUrl": user["thumbnailUrl"],
        "displayName": user["displayName"],
        "profileBackground": {"opacity": user["profileBackground"]["opacity"]},
        "photos": [
            {"value": photo["value"], "type": photo["type"]} for photo in user["photos"]
        ],
        "accounts": [
            {
                "domain": account["domain"],
                "display": account["display"],
                "url": account["url"],
                "iconUrl": account["iconUrl"],
                "username": account["username"],
                "verified": account["verified"],
                "name": account["name"],
                "shortname": account["shortname"],
            }
            for account in user["accounts"]
        ],
    }
    return gravatar_profile


# preferred_username = data["entry"][0]["preferredUsername"]
# display_name = data["entry"][0]["displayName"]
# print(preferred_username)
# print(display_name)
