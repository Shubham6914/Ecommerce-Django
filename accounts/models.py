from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.


'''class for creating the custom user using djangi baseusermanage field  '''
class MyaccountManager(BaseUserManager):
   def create_user(self,first_name,last_name,email,username,password=None):
      if not email:
         raise ValueError('user must have an email address')
      if not username:
         raise ValueError('user must have an username')
      
      user = self.model(
         email = self.normalize_email(email), # normalize make captial letter to lower
         username = username,
         first_name = first_name,
         last_name = last_name,
      )

      user.set_password(password)  # for setting the password we used set.password here
      user.is_active = True
      user.is_staff = True
      user.save(using = self.db)
      return user
   
   #this function is used to create a super user with the help of create_user fucntion
   def create_superuser(self,first_name,last_name,email,username,password):
      user = self.create_user(
         email = self.normalize_email(email),
         username = username,
         password = password,
         first_name = first_name,
         last_name = last_name,
      )
      '''this is superUser so here we are giving all permission to the superuser'''
      user.is_admin = True
      user.is_active = True
      user.is_staff = True
      user.is_superadmin = True
      user.save(using = self.db)
      return user


class Account(AbstractBaseUser): #creating base user
   first_name   = models.CharField(max_length=50)
   last_name    = models.CharField(max_length=50)
   username     = models.CharField(max_length=50,unique=True)
   email        = models.EmailField(max_length=90,unique=True)
   phone_number = models.CharField(max_length=40)

   # required fields for user
   date_joined       = models.DateTimeField(auto_now_add=True)
   last_login        = models.DateTimeField(auto_now_add=True)
   is_admin          = models.BooleanField(default=False)
   is_staff          = models.BooleanField(default=False)
   is_active         = models.BooleanField(default=False) # Typically, new users are set as active by default
   is_superadmin     = models.BooleanField(default=False)

   USERNAME_FIELD = 'email'  #using this we will be able to login as email address
   REQUIRED_FIELDS = ['username','first_name','last_name'] #these are the required filds
   
   objects = MyaccountManager()

   def __str__(self):
      return self.email
   

   '''this has_perms(self,perm,obj=None) function is mandatory to use
   whenever we create a custom user this function define that admin has
   all permissions and he can make any changes in the admin panel '''

   def has_perm(self,perm,obj=None):
      return self.is_admin
   
   def has_module_perms(self,add_label):
      return True