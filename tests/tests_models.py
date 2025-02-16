from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from kitchen.models import DishType, Dish, Cook


class ModelsTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(
            name="test_type_name")
        self.assertEqual(
            str(dish_type), dish_type.name)

    def test_cook_str(self):
        cook = get_user_model().objects.create(
            username="Test cook",
            first_name="Cook first name",
            last_name="Cook last name",
        )

        self.assertEqual(
            str(cook),
            f"{cook.username} ({cook.first_name} {cook.last_name})"
        )

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="test_dish_name")
        dish = Dish.objects.create(
            name="test_username",
            price="10",
            dish_type=dish_type
        )
        self.assertEqual(
            str(dish),
            f"{dish.name}"
        )

    def test_cook_years_of_experience(self):
        with self.assertRaises(ValidationError):
            cook = Cook(
                username="new_chef",
                first_name="New",
                last_name="Chef",
                years_of_experience=0)
            cook.full_clean()
