from django.urls import path

from .views import ContactListView, ContactDetailView

urlpatterns = [
    path("contact/<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),
    path("", ContactListView.as_view(), name="contact_list"),
]
