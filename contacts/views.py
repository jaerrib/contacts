import pandas
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import FileResponse
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


def export_contact_list(request):
    query_set = Contact.objects.filter(creator=request.user.pk)

    data_dict = {
        "first_name": [],
        "last_name": [],
        "phone_number": [],
        "email": [],
    }
    for item in query_set:
        item_detail = Contact.objects.get(
            first_name=item.first_name, last_name=item.last_name
        )
        data_dict["first_name"].append(item_detail.first_name)
        data_dict["last_name"].append(item_detail.last_name)
        data_dict["phone_number"].append(item_detail.phone_number)
        data_dict["email"].append(item_detail.email)
    data = pandas.DataFrame(data_dict)
    creator_id = str(query_set[0].creator_id)
    filename = creator_id + "_exported_contacts.csv"
    data.to_csv("media/" + filename)
    return FileResponse(open("media/" + filename, "rb"), as_attachment=True)
