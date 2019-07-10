import logging

from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
# from myStock.core import async_tasks
# from myStock.core import helpers


LOG = logging.getLogger('myStock.%s' % __name__)


# Create your models here.


class UserManager(BaseUserManager):
    # use_in_migrations = True
    """
    Manager class deals with the creation of user and superuser
    """
    def create_user(self, email, password=None, username=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=UserManager.normalize_email(email),
            is_staff=True, is_active=True, is_superuser=False,
            last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    """
    Users within the Django authentication system are represented by this
    model.
    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), blank=False, unique=True, max_length=254)
    nick_name = models.CharField(_('nick name'), unique=False, max_length=30, help_text=_('Nick name of the user'))
    full_name = models.CharField(_('full name'), max_length=30, blank=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)


    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def has_changed(instance, field):
        if not instance.pk:
            return False
        old_value = instance.__class__._default_manager.filter(pk=instance.pk).values(field).get()[field]
        return not getattr(instance, field) == old_value


class Profile(models.Model):
    """
    Profile model to save user profile linked to Auth user by onetoone field.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.CharField(max_length=255, blank=True)
    profile_pic = models.FileField(upload_to='profile/', blank=True)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return self.user.email

    def has_changed(instance, field):
        if not instance.pk:
            return False
        old_value = instance.__class__._default_manager.filter(pk=instance.pk).values(field).get()[field]
        return not getattr(instance, field) == old_value


class Participants(models.Model):
    """

    """
    name = models.TextField(_('name'), help_text=_('Name of the Participant'))
    email = models.EmailField(_('email address'), blank=False, unique=True, max_length=254)
    phoneNumber = models.IntegerField(_('phone number'), blank=False, unique=True,)
    college = models.TextField(_('college'), help_text=_('College of the participant'))
    stream = models.TextField(_('stream'), help_text=_('Stream of the Participant'))
    subregion = models.TextField(_('subregion'), help_text=_('Subregion of the Participant'))
    zone = models.TextField(_('zone'), help_text=_('Zone of the Participant'))
    dob = models.DateField(_('date of birth'),  blank=True, null=True,  help_text=_('event date'))

    class Meta:
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super(Participants, self).save(*args, **kwargs)