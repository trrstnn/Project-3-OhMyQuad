import datetime
#import everything from peewee because we might need it 
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash



DATABASE = SqliteDatabase('ohmyquad.db')

class User(UserMixin, Model):
    __table_args__ = {'extend_existing': True} 
    
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    name = CharField()
    height = IntegerField()
    weight = IntegerField()
    goal = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
  
    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)
    
    #  function that creates a new user
    @classmethod
    def create_user(cls, username, email , password, name, height, weight, goal):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                name = name,
                height = height,
                weight = weight,
                goal = goal
            )
        except IntegrityError:
            raise ValueError("User already exists")

class Workout(Model):
    name = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref="workouts") 
    description = CharField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


class Exercise(Model):
    name=CharField()
    reps=IntegerField()
    sets=IntegerField()
    description=TextField()
    type=CharField()

    class Meta:
        database = DATABASE


class WorkoutExercise(Model):
    exercise = ForeignKeyField(Exercise) 
    workout = ForeignKeyField(Workout) 

    class Meta:
        database = DATABASE






def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Exercise,Workout,WorkoutExercise,User], safe=True)
    DATABASE.close()