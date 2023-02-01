from django.db import models
from amazon_backend_api.manager import AmazonuserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from amazon_backend_api.api.utils import INDIAN_STATES


STATE_CHOICES = ( (state,INDIAN_STATES.get(state)) for state in INDIAN_STATES )


class Amazonuser(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AmazonuserManager()

    def __str__(self):
        return self.email


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class UserAddress(BaseModel):

    user = models.ForeignKey(Amazonuser, on_delete=models.CASCADE, verbose_name="User")
    country = models.CharField(verbose_name='Country', choices=(('India','India'),), max_length=100)
    full_name = models.CharField(verbose_name='Full name (First and last name)', max_length=100)
    mobile_number = models.IntegerField(verbose_name='Mobile number')
    pincode = models.IntegerField(verbose_name='Pincode')
    flat = models.CharField(verbose_name='Flat, House no., Building, Company, Apartment', max_length=200)
    street = models.CharField(verbose_name='Area, Street, Sector, Village', max_length=200)
    landmark = models.CharField(verbose_name='Landmark', max_length=100)
    town = models.CharField(verbose_name='Town/City', max_length=100)
    state = models.CharField(verbose_name='State', choices=STATE_CHOICES, max_length=100)
    default = models.BooleanField(verbose_name='Make this my default address', default=False)
    address_type = models.CharField(verbose_name='Address Type', max_length=100, choices=(('Home','Home'),('Office','Office')))


    def __str__(self):
        return str(f'{self.full_name} Address')


class Brand(BaseModel):
    name = models.CharField(verbose_name='Brand Name', max_length=100)
    logo = models.ImageField(upload_to='brands/logo')

    def __str__(self):
        return str(f'{self.name}')


class Category(BaseModel):
    name = models.CharField(verbose_name='Category Name', max_length=100)

    def __str__(self):
        return str(f'{self.name}')


class Subcategory(BaseModel):
    name = models.CharField(verbose_name='SubCategory Name', max_length=100)

    def __str__(self):
        return str(f'{self.name}')


class Size(BaseModel):
    name = models.CharField(verbose_name='Size', max_length=100)

    def __str__(self):
        return str(f'{self.name}')
