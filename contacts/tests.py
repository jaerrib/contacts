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

    def test_url_exists_at_desired_location_detailview(self):
        response = self.client.get("/contact/1/")
        self.assertEqual(response.status_code, 200)

    def test_contact_listview(self):
        response = self.client.get(reverse("contact_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are not logged in")
        self.assertTemplateUsed(response, "contact_list.html")

    def test_contact_detail_view(self):
        response = self.client.get(
            reverse("contact_detail", kwargs={"pk": self.contact.pk})
        )
        no_response = self.client.get("/contact/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, self.contact.first_name)
        self.assertTemplateUsed(response, "contact_detail.html")

    def test_contact_create_view(self):
        response = self.client.post(
            reverse("new_contact"),
            {
                "first_name": "First",
                "last_name": "Last",
                "phone_number": "000-000-0000",
                "email": "firstlast@email.com",
                "creator": self.user.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.last().first_name, "First")
        self.assertEqual(Contact.objects.last().last_name, "Last")
        self.assertEqual(Contact.objects.last().phone_number, "000-000-0000")
        self.assertEqual(Contact.objects.last().email, "firstlast@email.com")

    def test_contact_update_view(self):
        response = self.client.post(
            reverse("contact_edit", args="1"),
            {
                "first_name": "Eric",
                "last_name": "Idle",
                "phone_number": "000-000-0001",
                "email": "ericidle@pythonic.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.last().first_name, "Eric")
        self.assertEqual(Contact.objects.last().last_name, "Idle")
        self.assertEqual(Contact.objects.last().phone_number, "000-000-0001")
        self.assertEqual(Contact.objects.last().email, "ericidle@pythonic.com")

    def test_contact_delete_view(self):
        response = self.client.post(reverse("contact_delete", args="1"))
        self.assertEqual(response.status_code, 302)
