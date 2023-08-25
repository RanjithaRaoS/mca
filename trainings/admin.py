from django.contrib import admin
from .models import WeightEntry, TrainingPlan, Training, Exercise, UserProfile

@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    # Customize WeightEntry admin if needed
    pass

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    # Customize TrainingPlan admin if needed
    pass

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    # Customize Training admin if needed
    pass

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    # Customize Exercise admin if needed
    pass

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Customize UserProfile admin if needed
    pass



