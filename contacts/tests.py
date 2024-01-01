from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from contacts.models import Contact


class ContactModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )

        cls.contact = Contact.objects.create(
            first_name="first",
            last_name="last",
            phone_number="000-000-0000",
            email="contacttest@email.com",
            creator=cls.user,
        )

    def test_contact_model(self):
        self.assertEqual(self.contact.first_name, "first")
        self.assertEqual(self.contact.last_name, "last")
        self.assertEqual(self.contact.phone_number, "000-000-0000")
        self.assertEqual(self.contact.email, "contacttest@email.com")
        self.assertEqual(self.contact.get_absolute_url(), "/contact/1/")

    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/contact/1/")
        self.assertEqual(response.status_code, 200)

    def test_contact_listview(self):
        response = self.client.get(reverse("contact_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contact.first_name)
        self.assertTemplateUsed(response, "contact_list.html")

    def test_contact_detailview(self):
        response = self.client.get(
            reverse("contact_detail", kwargs={"pk": self.contact.pk})
        )
        no_response = self.client.get("/contact/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, self.contact.first_name)
        self.assertTemplateUsed(response, "contact_detail.html")
