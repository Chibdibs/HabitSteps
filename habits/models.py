from django.db import models
from django.contrib.auth.models import User
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    redeemed_points = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class HabitSchedule(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])

    def __str__(self):
        return f"{self.habit.name} on {self.day_of_week}"


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    completed = models.BooleanField(default=False)


class DailyProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    completion_rate = models.FloatField()  # Percentage of habits completed
    points_earned = models.IntegerField(default=0)

    def __str__(self):
        return f"Progress for {self.user.username} on {self.date}"
