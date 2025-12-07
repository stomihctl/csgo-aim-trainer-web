from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class AccountDeletionRequest(models.Model):
    requestid = models.AutoField(db_column='requestId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('app.CustomUser', models.CASCADE, db_column='userId')  # Field name made lowercase.
    daterequested = models.DateField(db_column='dateRequested')  # Field name made lowercase.
    status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        db_table = 'account_deletion_request'


class Admin(models.Model):
    adminid = models.OneToOneField('app.CustomUser', models.CASCADE, db_column='adminId', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'admin'


class EntryTest(models.Model):
    testid = models.AutoField(db_column='testId', primary_key=True)  # Field name made lowercase.
    playerid = models.ForeignKey('Player', models.CASCADE, db_column='playerId')  # Field name made lowercase.
    datetaken = models.DateField(db_column='dateTaken')  # Field name made lowercase.
    score = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'entry_test'


class Exercise(models.Model):
    exerciseid = models.AutoField(db_column='exerciseId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    difficulty = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'exercise'


class ExerciseStat(models.Model):
    statid = models.AutoField(db_column='statId', primary_key=True)
    playerid = models.ForeignKey('Player', models.CASCADE, db_column='playerId')
    exerciseid = models.ForeignKey(Exercise, models.CASCADE, db_column='exerciseId')
    date = models.DateField()
    score = models.IntegerField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'exercise_stat'


class PlanItem(models.Model):
    planid = models.ForeignKey(
        'WeeklyPlan',
        on_delete=models.CASCADE,
        db_column='planId',
        related_name='plan_items'
    )
    exerciseid = models.ForeignKey(
        Exercise,
        on_delete=models.SET_NULL,
        db_column='exerciseId',
        null=True,
        blank=True
    )
    dayofweek = models.IntegerField(db_column='dayOfWeek')
    sets = models.IntegerField(blank=True, null=True)
    repetitions = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'plan_item'
        unique_together = (('planid', 'exerciseid', 'dayofweek'),)
        ordering = ['dayofweek']



class Player(models.Model):
    playerid = models.OneToOneField('app.CustomUser', models.CASCADE, db_column='playerId', primary_key=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=12, blank=True, null=True)
    chosentrainer = models.ForeignKey('Trainer', models.SET_NULL, db_column='chosenTrainer', blank=True, null=True)

    headshot = models.IntegerField(default=0)
    counterstrafing = models.IntegerField(default=0)
    spray = models.IntegerField(default=0)
    reactiontime = models.IntegerField(default=0)

    class Meta:
        db_table = 'player'


class Trainer(models.Model):
    trainerid = models.OneToOneField('app.CustomUser', models.CASCADE, db_column='trainerId', primary_key=True)
    expertise = models.CharField(max_length=100, blank=True, null=True)
    availability = models.CharField(max_length=11, blank=True, null=True)
    priceperhour = models.DecimalField(db_column='pricePerHour', max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'trainer'


class TrainerAttribute(models.Model):
    trainerid = models.OneToOneField(Trainer, models.CASCADE, db_column='trainerId', primary_key=True)
    level = models.CharField(max_length=12)

    class Meta:
        db_table = 'trainer_attribute'
        unique_together = (('trainerid', 'level'),)


class TrainerLanguage(models.Model):
    trainerid = models.OneToOneField(Trainer, models.CASCADE, db_column='trainerId', primary_key=True)
    language = models.CharField(max_length=30)

    class Meta:
        db_table = 'trainer_language'
        unique_together = (('trainerid', 'language'),)


class TrainingFeedback(models.Model):
    feedbackid = models.AutoField(db_column='feedbackId', primary_key=True)
    playerid = models.ForeignKey(Player, models.SET_NULL, db_column='playerId', null=True, blank=True)
    trainerid = models.ForeignKey(Trainer, models.SET_NULL, db_column='trainerId', null=True, blank=True)
    planid = models.ForeignKey('WeeklyPlan', models.SET_NULL, db_column='planId', blank=True, null=True)
    text = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'training_feedback'


class TrainingRequest(models.Model):
    requestid = models.AutoField(db_column='requestId', primary_key=True)
    playerid = models.ForeignKey(Player, models.SET_NULL, db_column='playerId', null=True, blank=True)
    trainerid = models.ForeignKey(Trainer, models.SET_NULL, db_column='trainerId', null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, default='pending', blank=True, null=True)

    class Meta:
        db_table = 'training_request'

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('player', 'Player'),
        ('coach', 'Coach'),
        ('admin', 'Administrator'),
    ]
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='player')

    class Meta:
        db_table = 'user'



class WeeklyPlan(models.Model):
    planid = models.AutoField(db_column='planId', primary_key=True)  # Field name made lowercase.
    trainerid = models.ForeignKey(Trainer, models.SET_NULL, db_column='trainerId', null=True, blank=True)  # Field name made lowercase.
    playerid = models.ForeignKey(Player, models.SET_NULL, db_column='playerId', null=True, blank=True)  # Field name made lowercase.
    creationdate = models.DateField(db_column='creationDate')  # Field name made lowercase.
    status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        db_table = 'weekly_plan'