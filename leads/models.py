from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# Create your models here.

class User(AbstractUser):
    is_organisor=models.BooleanField(default=True)
    is_agent=models.BooleanField(default=False)

class UserProfile(models.Model):
   user=models.OneToOneField(User,on_delete=models.CASCADE)

   def __str__(self):
       return self.user.username 

#These are the fields of the model, which store the data for each Lead instance 
# # The first_name and last_name fields are strings that store the name of the Lead 
# # The age field is an integer that stores the age of the Lead, with a default value of 0 
# # The agent field is a foreign key to the Agent model, which means that each Lead belongs to one Agent, and an Agent can have many Leads 
# # The on_delete argument specifies what happens when the related Agent is deleted. In this case, it uses models.CASCADE, which means that if the Agent is deleted, the Lead will also be deleted
class Lead(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    age=models.IntegerField(default=0)
    organisation=models.ForeignKey(UserProfile,related_name='leads',on_delete=models.CASCADE)
    agent=models.ForeignKey('Agent',related_name='leads',on_delete=models.SET_NULL,null=True,blank=True)
    category=models.ForeignKey('Category',related_name='leads',on_delete=models.SET_NULL,blank=True,null=True)
    description=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
    phone_number=models.CharField(max_length=20)
    email=models.EmailField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


# These are the fields of the model, which store the data for each Agent instance 
# # The user field is a one-to-one relationship with the User model, which means that each Agent can have only one User, and vice versa 
# # The organisation field is a foreign key to the UserProfile model, which means that each Agent belongs to one UserProfile, but a UserProfile can have many Agents 
# # The on_delete argument specifies what happens when the related User or UserProfile is deleted. In this case, it uses models.CASCADE, which means that if the User or UserProfile is deleted, the Agent will also be deleted
class Agent(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    organisation=models.ForeignKey(UserProfile,related_name='agents',on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.email
    

class Category(models.Model):
    name=models.CharField(max_length=100)
    organisation=models.ForeignKey(UserProfile,related_name='categories',on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self) -> str:
        return self.name


def post_user_created_signal(sender,instance,created,**kwargs):
   if created:
       UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal,sender=User)