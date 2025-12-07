
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Avg
from django.shortcuts import render, redirect
from .models import Trainer, Player, WeeklyPlan
from .models import TrainerAttribute
from django.db.models import Q
import random
from django.http import JsonResponse
from django.utils import timezone
from .models import Player, Exercise, ExerciseStat
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.

def login(request):
    """
    view for the login/register page(default page)

    :param request:
    :return:
    """

    if request.method == "POST":
        if request.POST.get("action") == "login":
            identifier = request.POST.get("identifier")
            password = request.POST.get("password")
            role=request.POST.get("role")

            user = authenticate(request, username=identifier, password=password)
            if not user:
                try:
                    user_obj = CustomUser.objects.get(email=identifier)
                    user = authenticate(request, username=user_obj.username, password=password)
                except CustomUser.DoesNotExist:
                    user = None

            if user:
                if user.role != role:
                    messages.error(request, "Roles do not match")
                    return redirect('/')
            else:
                messages.error(request, "Invalid credentials")
                return redirect('/')
            auth_login(request, user)
            if user.role == "player":
                try:
                    player = Player.objects.get(playerid = user)
                    entry_taken = EntryTest.objects.filter(playerid=player).exists()
                    if not entry_taken:
                        return redirect('/entry_test')
                except Player.DoesNotExist:
                    messages.error("Player does not exist")
                    return redirect('/')

            return redirect('home')
        elif request.POST.get("action") == "register":
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            password_confirm = request.POST.get("password_confirm")
            role = request.POST.get("role")

            if password != password_confirm:
                messages.error(request, "Passwords do not match.")
                return redirect("/")

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect("/")

            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return redirect("/")

                # Create user
            if role == 'admin':
                user = CustomUser.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    role=role
                )
                Admin.objects.create(adminid=user)

            else:
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,  # raw password, will be hashed automatically
                    role=role
                )
            if role == 'player':
                Player.objects.create(
                    playerid=user,
                    nickname=username,  # optional
                    age=None,
                    level=None,
                    chosentrainer=None
                )
            elif role == 'coach':
                Trainer.objects.create(
                    trainerid=user,
                    expertise=None,
                    availability=None,
                    priceperhour=None
                )
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("/")

    return render(request, 'login.html')


@login_required(login_url='/')
def entry_test(request):
    """
    view for the entry_test page
    should be displayed when the player registers to assess his skills
    :param request:
    :return:
    """
    if request.user.role != 'player':
        messages.error(request, "Only players can take an entry test")
        return redirect('/home')
    if request.method == "POST":
        score = int(request.POST.get("score", 0))
        reflex = int(request.POST.get("reflex", 0))
        try:
            player = Player.objects.get(playerid=request.user)
        except Player.DoesNotExist:
            return redirect('/home')
        EntryTest.objects.create(
            playerid=player,
            datetaken=timezone.now().date(),
            score=score+reflex
        )
        player.headshot=score+reflex
        player.counterstrafing=score+reflex
        player.spray=score+reflex
        player.reactiontime=score+reflex
        lvl=""
        if score+reflex<8:
            lvl="Beginner"
        else:
            lvl="Intermediate"
        player.level=lvl
        player.save()
        return redirect('/home')
    return render(request, 'entrytest.html')

@login_required(login_url='/')
def account_removal_request(request):
    if request.user.role != 'player':
        messages.error(request, "Only players can request account removal.")
        return redirect('home')

    if request.method == 'POST':
        # Check if a pending request already exists
        existing_request = AccountDeletionRequest.objects.filter(
            userid=request.user, status='Pending'
        ).first()
        if existing_request:
            messages.info(request, "You already have a pending account removal request.")
        else:
            # Create a new request
            AccountDeletionRequest.objects.create(
                userid=request.user,
                daterequested=timezone.now(),
                status='Pending'
            )

            messages.success(request, "Your account removal request has been submitted.")
    return redirect('home')

@login_required(login_url='/')
def account_remove(request):
    """
    view for the account_remove page
    :param request:
    :return:
    """
    if request.user.role != 'admin':
        messages.error(request, "Only admins can remove an account.")
        return redirect('/home')
    requests_list = AccountDeletionRequest.objects.all()
    if request.method == "POST":
        username_to_delete = request.POST.get('manual-username')
        if username_to_delete:
            try:
                user = CustomUser.objects.get(username=username_to_delete)
                if user.role == 'admin':
                    messages.error(request, "You cannot remove an admin account.")
                else:
                    # Delete related Player or Trainer entry first
                    if user.role == 'player':
                        Player.objects.filter(playerid=user).delete()
                    elif user.role == 'coach':
                        Trainer.objects.filter(trainerid=user).delete()

                    # Delete the user
                    user.delete()
                    messages.success(request, f"Account '{username_to_delete}' removed successfully!")
            except CustomUser.DoesNotExist:
                messages.error(request, f"Username: {username_to_delete} does not exist.")
        return redirect('/account_remove')

    return render(request, 'accountRemove.html', {'requests_list': requests_list})
@login_required(login_url='/')
def attributes_input(request):
    """
    view for the attributes_input page
    :param request:
    :return:
    """
    return render(request, 'attributesInput.html')
@login_required(login_url='/')
def request_training_plan(request):
    """
    view for the request_training_plan page
    :param request:
    :return:
    """
    if request.user.role != "player":
        messages.error(request, "Only players can request training plan.")
        return redirect('/home')
    player = Player.objects.get(playerid=request.user)
    trainer = player.chosentrainer

    if not trainer:
        messages.error(request, "You do not have a trainer assigned")
        return redirect('/home')

    # Check if there's already a pending training request for this player
    existing_request = TrainingRequest.objects.filter(
        playerid=player,
        status='pending'
    ).first()

    if existing_request:
        messages.info(request, "You already have a pending training request.")
        return redirect('home')

    existing_training_plan = WeeklyPlan.objects.filter(playerid=player, trainerid=trainer).first()
    if existing_training_plan:
        messages.info(request, "You already have a training plan")
        return redirect('/home')

    if request.method == "POST":
        comment = request.POST.get('comment').strip()

        TrainingRequest.objects.create(
            playerid=player,
            trainerid=trainer,
            comment=comment,
            date=timezone.now(),
            status='pending'
        )
        messages.success(request, f"Your training request has been submitted.")
        return redirect('/home')
    return render(request, 'requestTrainingPlan.html')

def reset_password(request):
    """
    view for the reset_password page
    :param request:
    :return:
    """
    return render(request, 'resetPassword.html')
@login_required(login_url='/')
def single_training_request(request):
    """
    view for the single_training_request page
    :param request:
    :return:
    """
    if request.user.role != 'player':
        messages.error(request, "Only players can remove an account.")
        return redirect('/home')
    exercises = Exercise.objects.all()
    exercise = ''
    if request.method == "POST":
        selectedExercise = request.POST.get('exerciseType')
        if selectedExercise != "":
            exercises = Exercise.objects.filter(type=selectedExercise)
        exercise = random.choice(exercises)

    return render(request, 'singleTrainingRequest.html', {'exercise': exercise})
@login_required(login_url='/')
def trainer_selection(request):
    trainers = Trainer.objects.all().select_related('trainerid')

    # Filters
    specialization = request.GET.get('specialization')
    language = request.GET.get('language')
    price_sort = request.GET.get('price')
    name_search = request.GET.get('name')

    # Filtriranje po specijalizaciji
    if specialization:
        trainers = trainers.filter(expertise__icontains=specialization)

    # Filtriranje po jeziku iz TrainerLanguage
    if language:
        trainers = trainers.filter(trainerlanguage__language__icontains=language)

    # Filtriranje po imenu
    if name_search:
        trainers = trainers.filter(trainerid__username__icontains=name_search)

    # Sortiranje po ceni
    if price_sort == "low":
        trainers = trainers.order_by('priceperhour')
    elif price_sort == "high":
        trainers = trainers.order_by('-priceperhour')

    # Dodaj u context i jezik i level za prikaz
    trainers_with_details = []
    for t in trainers:
        lang_obj = TrainerLanguage.objects.filter(trainerid=t).first()
        level_obj = TrainerAttribute.objects.filter(trainerid=t).first()
        trainers_with_details.append({
            'trainer': t,
            'language': lang_obj.language if lang_obj else "N/A",
            'level': level_obj.level if level_obj else "N/A",
        })

    context = {
        'trainers': trainers_with_details,
        'selected_specialization': specialization or "",
        'selected_language': language or "",
        'selected_price': price_sort or "",
        'name_search': name_search or "",
    }

    return render(request, 'trainerSelection.html', context)

@login_required(login_url='/')
def training_plan_generation(request):
    """
    view for the training_plan_generation page
    :param request:
    :return:
    """
    return render(request, 'trainingPlanGeneration.html')
@login_required(login_url='/')
def training_statistics(request):
    if request.user.role != 'player':
        messages.error(request, "Only players can enter exercise statistics.")
        return redirect('home')

    player = Player.objects.get(playerid=request.user)
    exercises = Exercise.objects.all()

    if request.method == "POST":
        exercise_id = request.POST.get("exercise")
        score = request.POST.get("score")
        duration = request.POST.get("time")
        notes = request.POST.get("notes")

        if not exercise_id or not score or not duration:
            messages.error(request, "Please fill in all required fields.")
            return redirect('training_statistics')

        try:
            exercise = Exercise.objects.get(exerciseid=exercise_id)
        except Exercise.DoesNotExist:
            messages.error(request, "Selected exercise does not exist.")
            return redirect('training_statistics')

        type = exercise.type
        score = int(score)
        old_score = score
        if type == 'headshot':
            old_score = player.headshot
            value = old_score * 0.8 + score * 0.2
            player.headshot = int(value)
        elif type == 'counterstrafing':
            old_score = player.counterstrafing
            value = old_score * 0.8 + score * 0.2
            player.counterstrafing = int(value)
        elif type == 'spray':
            old_score = player.spray
            value = old_score * 0.8 + score * 0.2
            player.spray = int(value)
        elif type == 'reactiontime':
            old_score = player.reactiontime
            value = old_score * 0.8 + score * 0.2
            player.reactiontime = int(value)

        player.save()
        from datetime import time
        dur_minutes = int(duration)
        dur_time = time(hour=dur_minutes // 60, minute=dur_minutes % 60)

        ExerciseStat.objects.create(
            playerid=player,
            exerciseid=exercise,
            date=timezone.now().date(),
            score=int(score),
            duration=dur_time,
            notes=notes or ""
        )
        messages.success(request, "Exercise statistics successfully saved!")
        return redirect('training_statistics')

    context = {'exercises': exercises}
    return render(request, 'trainingStatistics.html', context)


@login_required(login_url='/')
def logoff(request):
    """
    helper view for the logoff page
    :param request:
    :return:
    """
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def home(request):
    context = {
        'num_trainers': Trainer.objects.count(),
        'num_players': Player.objects.count(),
        'num_plans': WeeklyPlan.objects.count(),
        'avg_price': Trainer.objects.aggregate(Avg('priceperhour'))['priceperhour__avg'] or 0,
        'top_trainers': Trainer.objects.all()[:5],
    }

    if request.user.role == 'player':
        context['message'] = "Find your perfect CS2 coach and level up your gameplay!"
        context['show_search_link'] = True

        player = Player.objects.filter(playerid=request.user).first()
        if player and player.chosentrainer:
            context['chosen_trainer'] = player.chosentrainer.trainerid.username
        else:
            context['chosen_trainer'] = None
        plan = WeeklyPlan.objects.filter(playerid=request.user.id).first()
        if request.method == "POST":
            days = PlanItem.objects.filter(planid=plan).delete()
            WeeklyPlan.objects.filter(playerid=request.user.id).delete()
        if plan:
            plan = plan.planid
            days = PlanItem.objects.filter(planid=plan)
            week = []
            for day in days:
                week.append(Exercise.objects.filter(exerciseid=day.exerciseid.exerciseid).first())
            context['week'] = week
        context['player'] = Player.objects.get(playerid=request.user)

    elif request.user.role == 'coach':
        trainer = Trainer.objects.filter(trainerid=request.user).first()
        language = TrainerLanguage.objects.filter(trainerid=trainer).first()
        level = TrainerAttribute.objects.filter(trainerid=trainer).first()

        players = Player.objects.filter(chosentrainer__trainerid=request.user.id)

        players_with_requests = []
        for p in players:
            has_request = TrainingRequest.objects.filter(playerid=p, trainerid=trainer, status='pending').exists()
            players_with_requests.append((p, has_request))
        context['trainer'] = trainer
        context['trainer_language'] = language.language if language else ''
        context['trainer_level'] = level.level if level else ''
        context['players'] = players
        context['players_with_requests'] = players_with_requests

    elif request.user.role == 'admin':
        context['message'] = "Manage users and monitor platform statistics."



    return render(request, 'home.html', context)


@login_required(login_url='/')
def update_trainer_profile(request):
    if request.user.role != 'coach':
        messages.error(request, "Only coaches can edit this section.")
        return redirect('home')

    trainer = Trainer.objects.get(trainerid=request.user)
    language_obj, _ = TrainerLanguage.objects.get_or_create(trainerid=trainer)
    level_obj, _ = TrainerAttribute.objects.get_or_create(trainerid=trainer)

    if request.method == "POST":
        trainer.expertise = request.POST.get('expertise', '')
        trainer.availability = request.POST.get('availability', '')
        trainer.priceperhour = request.POST.get('priceperhour', 0)
        trainer.save()

        language_obj.language = request.POST.get('language', '')
        language_obj.save()

        level_obj.level = request.POST.get('level', '')
        level_obj.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('home')

    return redirect('home')

@login_required(login_url='/')
def choose_trainer(request, trainer_id):
    if request.user.role != 'player':
        messages.error(request, "Only players can choose a trainer.")
        return redirect('home')

    try:
        trainer = Trainer.objects.get(trainerid__id=trainer_id)
    except Trainer.DoesNotExist:
        messages.error(request, "Trainer not found.")
        return redirect('trainer_selection')

    player = Player.objects.get(playerid=request.user)
    player.chosentrainer = trainer
    player.save()

    messages.success(request, f"You have successfully chosen {trainer.trainerid.username} as your coach!")
    return redirect('home')

@login_required(login_url='/')
def remove_chosen_trainer(request):
    if request.user.role != 'player':
        messages.error(request, "Only players can remove a trainer.")
        return redirect('home')

    player = Player.objects.get(playerid=request.user)
    if player.chosentrainer:
        trainer_name = player.chosentrainer.trainerid.username
        player.chosentrainer = None
        player.save()
        messages.success(request, f"You have removed {trainer_name} as your trainer.")
    else:
        messages.info(request, "You do not have a trainer to remove.")

    return redirect('home')

@login_required(login_url='/')
def request_training_plan_for_player(request, player_id):
    if request.user.role != 'coach':
        messages.error(request, "Only coaches can assign training.")
        return redirect('home')

    try:
        player = Player.objects.get(playerid=player_id)
        trainer = Trainer.objects.get(trainerid=request.user)
    except Player.DoesNotExist:
        messages.error(request, "Player not found.")
        return redirect('home')

    exercises = Exercise.objects.all().order_by('name')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if request.method == "POST":
        # Create a new weekly plan
        plan = WeeklyPlan.objects.create(
            trainerid=trainer,
            playerid=player,
            creationdate=timezone.now(),
            status='active'
        )
        print(request.POST)

        for i in range(7):
            exercise_id = request.POST.get(f'day_{i}_exercise')
            sets = request.POST.get(f'day_{i}_sets')
            reps = request.POST.get(f'day_{i}_reps')

            print(f"Day {i + 1}: exercise_id={exercise_id}, sets={sets}, reps={reps}")

            if exercise_id:
                try:
                    exercise = Exercise.objects.get(exerciseid=int(exercise_id))
                except (Exercise.DoesNotExist, ValueError):
                    messages.error(request, "Exercise not found.")
                    WeeklyPlan.objects.filter(playerid=player,trainerid=trainer).delete()
                    return redirect('home')


                PlanItem.objects.create(
                    planid=plan,
                    exerciseid=exercise,
                    dayofweek=i + 1,  # 1 = Monday
                    sets=int(sets) if sets else 0,
                    repetitions=int(reps) if reps else 0
                )

        TrainingRequest.objects.filter(playerid=player, trainerid=trainer).delete()
        messages.success(request, f"Weekly plan for {player.nickname} created successfully!")
        return redirect('home')

    context = {
        'player': player,
        'trainer': trainer,
        'exercises': exercises,
        'days': days
    }

    return render(request, 'trainingPlanGeneration.html', context)


