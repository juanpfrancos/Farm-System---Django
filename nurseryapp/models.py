from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

class Producer(models.Model):
    identity_document = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        # Esta función se llama durante la validación del modelo
        if not self.email or '@' not in self.email:
            raise ValidationError({'email': 'Invalid email address'})
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()  # Esto llama a clean() antes de guardar
        super().save(*args, **kwargs)

class Farm(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='farms')
    cadastral_number = models.CharField(max_length=50, unique=True)
    municipality = models.CharField(max_length=100)

class Nursery(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='nurseries')
    code = models.CharField(max_length=50)
    crop_type = models.CharField(max_length=100)

class Task(models.Model):
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE, related_name='tasks')
    date = models.DateField()
    description = models.TextField()

class ControlProduct(models.Model):
    ica_registration = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    application_frequency = models.IntegerField(help_text="Frequency in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

class FungusControl(ControlProduct):
    withdrawal_period = models.IntegerField(help_text="Withdrawal period in days")
    fungus_name = models.CharField(max_length=100)

class PestControl(ControlProduct):
    withdrawal_period = models.IntegerField(help_text="Withdrawal period in days")

class FertilizerControl(ControlProduct):
    last_application_date = models.DateField()

class ProductApplication(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='applications')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')
    application_date = models.DateField()