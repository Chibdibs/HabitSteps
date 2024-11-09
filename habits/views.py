from django.shortcuts import render, redirect
from django.utils import timezone
from .models import UserProfile, Habit, HabitLog, HabitSchedule, DailyProgress
from datetime import date


def home(request):
    return render(request, 'home.html')


def complete_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    log, created = HabitLog.objects.get_or_create(habit=habit, date=date.today())
    log.completed = True
    log.save()

    update_daily_progress(request.user)
    return redirect('dashboard')


def update_daily_progress(user):
    habits = Habit.objects.filter(user=user)
    today_scheduled_habits = habits.filter(habitschedule__day_of_week=date.today().strftime('%A'))

    completed_habits = HabitLog.objects.filter(
        habit__in=today_scheduled_habits, date=date.today(), completed=True
    ).count()
    completion_rate = completed_habits / today_scheduled_habits.count() if today_scheduled_habits else 0

    progress, created = DailyProgress.objects.get_or_create(user=user, date=date.today())
    progress.completion_rate = completion_rate * 100  # as a percentage
    progress.points_earned += int(completion_rate * 10)  # e.g., 10 points for 100% completion
    progress.save()

    profile = UserProfile.objects.get(user=user)
    if completion_rate == 1:
        profile.current_streak += 1
        if profile.current_streak > profile.longest_streak:
            profile.longest_streak = profile.current_streak
    else:
        profile.current_streak = 0
    profile.save()


def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    progress_data = DailyProgress.objects.filter(user=request.user).order_by('-date')[:7]

    dates = [progress.date.strftime('%Y-%m-%d') for progress in progress_data]
    completion_rates = [progress.completion_rate for progress in progress_data]

    context = {
        'profile': user_profile,
        'dates': dates,
        'completion_rates': completion_rates,
    }
    return render(request, 'dashboard.html', context)
