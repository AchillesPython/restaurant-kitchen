from unittest import TestCase


from kitchen.forms import CookCreateForm, DishSearchForm


class FormsTest(TestCase):
    def test_check_valid_creation_form(self):
        form_data = {
            "username": "new_user",
            "password1": "new_user_password",
            "password2": "new_user_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "years_of_experience": 3,
        }
        form = CookCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DishSearchFormTest(TestCase):
    def test_search_form_valid_data(self):
        form_data = {'name': 'Pizza'}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_blank_data(self):
        form_data = {}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_invalid_data(self):
        form_data = {'name': 'A' * 64}
        form = DishSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_search_form_rendering(self):
        form = DishSearchForm()
        self.assertIn('placeholder="Search by name"', str(form))
