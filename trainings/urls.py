from django.urls import path
from .views import trainings_view, single_training_view, start_training_view, stop_training_view,  add_exercises_to_training_view, training_progress, record_weight, weight_progress, user_profile,register ,create_training_view
from django.contrib.auth.views import LoginView

# edit_training_view, start_training, stop_training, \
# delete_training, cancel_training, record_training, add_exercise_to_training, \
# save_training_plan, load_training_plan,


urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # Redirect to the login view
    path('register/', register, name='register'),
    path('base/', trainings_view, name='base'),  # main page shows trainings/
    path('trainings/', trainings_view, name='trainings'),
    path('trainings/<int:training_id>/', single_training_view, name='single_training_view'),
    path('trainings/<int:training_id>/start/', start_training_view, name='start_training'),
    path('trainings/<int:training_id>/stop/', stop_training_view, name='stop_training'),

    path('add_exercises_to_training/<int:training_id>/', add_exercises_to_training_view, name='add_exercises_to_training'),
    path('training-progress/',training_progress, name='training_progress'),
    path('record-weight/', record_weight, name='record_weight'),
    path('weight-progress/', weight_progress, name='weight_progress'),
    path('user-profile/', user_profile, name='user_profile'),
    path('create-training/', create_training_view, name='create_training'),
    # path('single-training/', single_training_view, name='single_training_view')
]


# path('edit-training/<int:training_id>/', edit_training_view),
    # path('record-training/', record_training),
# path('save-training/<int:training_id>/', save_training),
    # path('delete-training/<int:training_id>/', delete_training),
    # path('cancel-training/<int:training_id>/', cancel_training),
# path('save-training-plan/<int:training_id>/', save_training_plan),
    # path('load-training-plan/<int:training_id>/', load_training_plan),


