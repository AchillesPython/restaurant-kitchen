from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)

from kitchen.forms import (
    DishTypeForm,
    CookCreateForm,
    DishForm,
    DishSearchForm,
    CookUpdateForm,
)
from kitchen.models import Cook, Dish, DishType


class IndexView(LoginRequiredMixin, ListView):
    template_name = "kitchen/index.html"
    context_object_name = "context"

    def get_queryset(self):
        num_cooks = Cook.objects.count()
        num_dishes = Dish.objects.count()
        num_dish_types = DishType.objects.count()

        num_visits = self.request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1

        return [
            {
                "num_cooks": num_cooks,
                "num_dishes": num_dishes,
                "num_dish_types": num_dish_types,
                "num_visits": num_visits + 1,
            }
        ]


class DishTypeListView(LoginRequiredMixin, ListView):
    model = DishType
    paginate_by = 2
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"


class DishTypeCreateView(LoginRequiredMixin, CreateView):
    model = DishType
    form_class = DishTypeForm
    success_url = reverse_lazy("kitchen:dish_type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish_type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish_type-list")


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")
    template_name = "kitchen/dish_form.html"


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish


class CookListView(LoginRequiredMixin, ListView):
    model = Cook
    paginate_by = 2


class CookDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "kitchen/cook_detail.html"
    queryset = get_user_model().objects.prefetch_related("dishes", "dishes__dish_type")


class CookCreateView(LoginRequiredMixin, CreateView):
    model = Cook
    form_class = CookCreateForm
    success_url = reverse_lazy("kitchen:cook-list")


class CookUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CookUpdateForm

    success_url = reverse_lazy("kitchen:cook-list")

    def form_valid(self, form):
        cook = form.save(commit=False)
        cook.dishes.clear()
        for dish in form.cleaned_data["dishes"]:
            cook.dishes.add(dish)
        cook.save()
        return super().form_valid(form)


class CookDeleteView(LoginRequiredMixin, DeleteView):
    model = Cook
    template_name = "kitchen/cook_confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")
