from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import Dish, DishType

DISH_TYPE_URL = reverse("kitchen:dish_type-list")
DISH_URL = reverse("kitchen:dish-list")
COOK_URL = reverse("kitchen:cook-list")


class PublicDishTypeTests(TestCase):

    def test_login_required(self):
        res = self.client.get(DISH_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_type(self):
        response = self.client.get(DISH_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]),
            list(dish_types),
        )
        self.assertTemplateUsed(response, "kitchen/dish_type_list.html")


class PublicDishTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(DISH_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDishTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_dishes(self):
        dish_type = DishType.objects.create(name="dish_type_test")
        Dish.objects.create(name="test_dish", price=5, dish_type=dish_type)
        response = self.client.get(DISH_URL)
        self.assertEqual(response.status_code, 200)

        dishes = Dish.objects.all()
        self.assertEqual(
            list(response.context["dish_list"]),
            list(dishes),
        )
        self.assertTemplateUsed(response, "kitchen/dish_list.html")

    def test_search_dish_by_name(self) -> None:
        """Test that we can find Dish by name"""
        self.search_name = "test"
        response = self.client.get(DISH_URL, {"name": self.search_name})
        context_dashes = Dish.objects.filter(name__icontains=self.search_name)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["dish_list"],
            context_dashes,
        )


class PublicCookTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(COOK_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCookTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test123124",
            password="14uhd1d1d",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

    def test_create_cook(self):
        form_data = {
            "username": "test_user",
            "password1": "test_password",
            "password2": "test_password",
            "first_name": "test_first_name",
            "last_name": "testing_last_name",
            "years_of_experience": 3,
        }
        self.client.post(reverse("kitchen:cook-create"), form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.years_of_experience, form_data["years_of_experience"])
