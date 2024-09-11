from django.db import models

class Producer(models.Model):
    identity_document = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

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
    product = models.ForeignKey(ControlProduct, on_delete=models.CASCADE)
    application_date = models.DateField()