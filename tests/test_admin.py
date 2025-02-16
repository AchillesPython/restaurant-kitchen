from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test_admin",
            years_of_experience=1
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="tester12",
            years_of_experience=1,
        )

    def test_cook_years_of_experience_listed(self):
        """
        test that cook's experience is listed in admin page
        """
        url = reverse("admin:kitchen_cook_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_years_of_experience_listed_detail(self):
        """
        test that cook's experience is listed in cook detail admin page
        """
        url = reverse("admin:kitchen_cook_change", args=[self.cook.id])
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_add_fieldsets(self):
        """
        Test that cook's first, last name
        & years_of_experience is on driver add page

        """
        url = reverse("admin:kitchen_cook_add")
        response = self.client.get(url)
        self.assertContains(response, "first_name")
        self.assertContains(response, "last_name")
        self.assertContains(response, "years_of_experience")
