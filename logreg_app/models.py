from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
FNAME_REGEX = re.compile(r'^[a-zA-Z\s]*$')
LNAME_REGEX = re.compile(r'^[a-zA-Z\s]*$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        
        if len(postData['firstname']) < 2 or len(postData['firstname']) > 25:
            errors["firstname"] = "First Name should be between 2 and 25 characters!"

        if not FNAME_REGEX.match(postData['firstname']):        
            errors['firstname'] = "First Name must be in a valid format!"

        if len(postData['lastname']) < 2 or len(postData['lastname']) > 25:
            errors["lastname"] = "Last Name should be between 2 and 25 characters!"

        if not LNAME_REGEX.match(postData['lastname']):        
            errors['lastname'] = "First Name must be in a valid format!"

        if not EMAIL_REGEX.match(postData['email']):        
            errors['email'] = "Email must be in a valid format!"

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters!"

        if postData['password'] != postData['confirm']:
            errors['confirm'] = "Password and Confirm PW must match!"
        
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['log_email'])
        if len(user) < 1:
            errors['log_email'] = "Invalid Credentials"
        else:
            logged_user = user[0] 
            if not bcrypt.checkpw(postData['pword'].encode(), logged_user.password.encode()):
                errors['log_email'] = "Invalid Credentials"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=26)
    last_name = models.CharField(max_length=26)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
