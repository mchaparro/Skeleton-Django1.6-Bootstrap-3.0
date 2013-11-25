# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

class UsuariosManager(BaseUserManager):
    def create_user(self, email, password="", nombre=""):
        """
        Creates and saves user with the given username and password.
        """
        if not email:
            raise ValueError('Favor de proporcionar un correo valido')

        usuario = self.model(
            email=UserManager.normalize_email(email),nombre=nombre
        )
        
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email="",password="",nombre=""):
        """
        Creates and saves a superuser with the given username
        """
        usuario = self.create_user(email=email,nombre=nombre,password=password)
        usuario.is_superuser = True
        usuario.is_admin = True
        usuario.save(using=self._db)
        return usuario

class Usuario(AbstractBaseUser, PermissionsMixin):
    usuario = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_mod = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UsuariosManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos']
    

    def __unicode__(self):
        return self.nombre

    @property
    def is_staff(self):
        # Handle whether the user is a member of staff"
        return self.is_admin
    
    #replace with your app name
    class Meta:
        app_label = 'skeleton'
