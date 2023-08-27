from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user


class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    started = models.DateTimeField( default=timezone.now)
    ended = models.DateTimeField( default=timezone.now)
    duration= models.IntegerField(blank=True, null=True,default=0)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE,default=None)
    name = models.TextField(default='Exercise')
    weight_kg = models.FloatField(blank=True, null=True, default=0)
    weight_per = models.TextField(blank=True, null=True,default='total')
    series = models.IntegerField(blank=True, null=True,default=0)
    reps = models.JSONField(blank=True, null=True,default=dict)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    foods = models.ManyToManyField(FoodItem, through='MealFood')

    def __str__(self):
        return self.name

class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Meal Foods'

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    meals = models.ManyToManyField(Meal, through='MealPlanMeal')

    def __str__(self):
        return self.name

class MealPlanMeal(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']






# class TrainingPlan(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
#     name = models.TextField()
#     exercises = models.JSONField()
#     """ exercises is table of dicts, e.g.,
#         exercises = [{'name': 'pushup', 'weight_kg': 5,
#                       'weight_per': 'total', 'series': 3},
#                       {'name': 'hammer', 'weight_kg': 5,
#                       'weight_per': 'per hand', 'series': 3}]
#
#     """
#     def __str__(self):
#         return self.name

class TrainingPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.TextField()
    trainings = models.ManyToManyField(Training)  # Many-to-many relationship with Training

    # Other fields as needed
    def __str__(self):
        return self.name  # Use a many-to-many relationship



class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(default=timezone.now())

    def __str__(self):
        return f"{self.timestamp} - {self.weight} kg"
