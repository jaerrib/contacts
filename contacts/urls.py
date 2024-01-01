from django.urls import path

from .views import (
    ContactListView,
    ContactDetailView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView,
)

urlpatterns = [
    path("contact/new/", ContactCreateView.as_view(), name="new_contact"),
    path("contact/<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),
    path("contact/<int:pk>/edit", ContactUpdateView.as_view(), name="contact_edit"),
    path("contact/<int:pk>/delete", ContactDeleteView.as_view(), name="contact_delete"),
    path("", ContactListView.as_view(), name="contact_list"),
]
