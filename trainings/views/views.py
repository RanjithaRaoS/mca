
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Avg
from ..models import Training, Exercise, TrainingPlan, WeightEntry
from ..forms import AddExercisesForm, TrainingForm
from django.utils import timezone
from django import forms
from django.db.models import Sum
from plotly.offline import plot
import plotly.graph_objects as go
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import plotly.graph_objs as go
from plotly.subplots import make_subplots



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

@login_required
def dashboard(request):
    return render(request, 'base.html')


@login_required
def user_profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'user_profile.html', context)

@login_required
def record_weight(request):
    if request.method == 'POST':
        new_weight = request.POST.get('weight')  # You'll get this from your form
        new_date = request.POST.get('date')
        user = request.user
        # Convert the date string to a datetime object
        formatted_date = datetime.strptime(new_date, '%Y-%m-%d')
        WeightEntry.objects.create(weight=new_weight, timestamp=formatted_date, user=user, date= formatted_date)
        # Get the list of weight entries
        weight_entries = WeightEntry.objects.all().order_by('-timestamp')
        context = {'weight_entries': weight_entries}
        return render(request, 'record_weight.html', context)
    else:
        weight_entries = WeightEntry.objects.all().order_by('-timestamp')
        context = {'weight_entries': weight_entries}
        return render(request, 'record_weight.html', context)


@login_required
def weight_progress(request):
    weight_entries = WeightEntry.objects.all().order_by('timestamp')

    # Prepare data for the chart
    timestamps = [entry.timestamp for entry in weight_entries]
    weights = [entry.weight for entry in weight_entries]

    # Create a line chart using Plotly
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(x=timestamps, y=weights, mode='lines+markers', name='Weight'))

    chart_div = fig.to_html(full_html=False, default_height=400)

    context = {'chart_div': chart_div}
    return render(request, 'weight_progress.html', context)

def create_training_view(request):
    if request.method == 'POST':
        print("entering post request")
        training_form = TrainingForm(request.POST)
        if training_form.is_valid():
            print("Form is valid")
            training = training_form.save(commit=False)
            training.user = request.user
            training.save()
            print( "trainign Id is", training.id
            )
            return redirect('add_exercises_to_training', training_id=training.id)
        else:
            print(training_form.errors)
    else:
        training_form = TrainingForm()

    context = {'training_form': training_form}
    return render(request, 'create-training.html', context)

from django.forms import formset_factory


def add_exercises_to_training_view(request, training_id):
    training = Training.objects.get(id=training_id)

    ExerciseFormSet = formset_factory(AddExercisesForm, extra=1)

    if request.method == 'POST':
        formset = ExerciseFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('exercise_name'):
                    exercise = Exercise(
                        training=training,
                        name=form.cleaned_data['exercise_name'],
                        weight_kg=form.cleaned_data['weight_kg'],
                        weight_per=form.cleaned_data['weight_per'],
                        series=form.cleaned_data['series'],
                        reps=form.cleaned_data['reps']
                    )
                    exercise.save()

            # Redirect to the desired page after adding exercises
            return redirect('base')  # Change 'dashboard' to the appropriate URL name
    else:
        formset = ExerciseFormSet()

    return render(
        request,
        'add_exercises_to_training.html',
        {'formset': formset, 'training': training}
    )



def start_training_view(request, training_id):
    print("getting inside start training")
    training = Training.objects.get(id=training_id)
    training.started = timezone.now()
    training.save()
    print(training.started)
    return redirect('single_training_view', training_id=training_id)

def stop_training_view(request, training_id):

    training = Training.objects.get(id=training_id)
    training.ended = timezone.now()
    elapsed_time = training.ended - training.started
    training.duration = elapsed_time.total_seconds() // 60
    training.save()
    return redirect('single_training_view', training_id=training_id)

def trainings_view(request):
    user = request.user
    trainings = Training.objects.filter(user=user)
    return render(request, 'trainings.html', {'trainings': trainings})

def single_training_view(request, training_id):
    training = get_object_or_404(Training, id=training_id)
    exercises = Exercise.objects.filter(training=training)
    # Calculate duration
    duration = training.ended - training.started
    duration_minutes = duration.total_seconds() // 60  # Convert to minutes

    return render(request, 'single_training_view.html', {
        'training': training,
        'exercises': exercises,
        'duration_minutes': duration_minutes})


import plotly.graph_objs as go
from django.db.models import Avg

def training_progress(request):
    trainings = Training.objects.all()

    training_data = []
    for training in trainings:
        if training.started and training.ended:
            duration = (training.ended - training.started).seconds // 60  # Duration in minutes
            avg_weight = training.exercises.aggregate(Avg('weight_kg'))['weight_kg__avg']
            dates = training.started
            training_data.append({
                'name': training.name,
                'duration': duration,
                'avg_weight': avg_weight,
                'dates': dates,
            })

    progress_chart = get_duration_plot(training_data)
    weight_chart = get_weight_plot(training_data)

    return render(request, 'training-progress.html', {
        'training_data': training_data,
        'progress_chart': progress_chart.to_html(full_html=False),
        'weight_chart': weight_chart.to_html(full_html=False),
    })

def get_duration_plot(training_data):
    training_names = [training['name'] for training in training_data]
    durations = [training['duration'] for training in training_data]

    return go.Figure(data=[go.Bar(x=training_names, y=durations)])

def get_weight_plot(training_data):
    training_names = [training['name'] for training in training_data]
    avg_weights = [training['avg_weight'] for training in training_data]

    return go.Figure(data=[go.Bar(x=training_names, y=avg_weights)])


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..models import Meal, MealFood, FoodItem, MealPlan, MealPlanMeal


@login_required
def create_meal_plan_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        meal_plan = MealPlan.objects.create(user=request.user, name=name)
        return redirect('add_meals_to_meal_plan', meal_plan_id=meal_plan.id)
    return render(request, 'create_meal_plan.html')


@login_required
def add_meals_to_meal_plan_view(request, meal_plan_id):
    meal_plan = MealPlan.objects.get(id=meal_plan_id)
    meals = Meal.objects.filter(user=request.user)

    if request.method == 'POST':
        selected_meals = request.POST.getlist('selected_meals')
        for order, meal_id in enumerate(selected_meals, start=1):
            MealPlanMeal.objects.create(meal_plan=meal_plan, meal_id=meal_id, order=order)
        return redirect('view_meal_plan', meal_plan_id=meal_plan.id)

    return render(request, 'add_meals_to_meal_plan.html', {'meal_plan': meal_plan, 'meals': meals})


@login_required
def view_meal_plan_view(request, meal_plan_id):
    meal_plan = MealPlan.objects.get(id=meal_plan_id)
    meal_plan_meals = MealPlanMeal.objects.filter(meal_plan=meal_plan)
    return render(request, 'view_meal_plan.html', {'meal_plan': meal_plan, 'meal_plan_meals': meal_plan_meals})

