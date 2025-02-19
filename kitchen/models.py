from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

from kitchen_service import settings


class DishType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        verbose_name = "dish type"
        verbose_name_plural = "dish types"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        ordering = ["-years_of_experience"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="dishes"
    )
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dishes")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "dishes"
        ordering = ("name",)


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"
