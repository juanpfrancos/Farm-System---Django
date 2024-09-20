from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from .models import Producer, Farm, Nursery, Task, ProductApplication, FungusControl

# Pruebas para el modelo Producer (Productor)
class ProducerTestCase(TestCase):
    def setUp(self):
        # Crear un productor de ejemplo para usar en las pruebas
        self.producer = Producer.objects.create(
            identity_document="1234567890",
            first_name="Juan",
            last_name="Pérez",
            phone="1234567890",
            email="juan@example.com"
        )

    def test_producer_creation(self):
        # Verificar que el productor se crea correctamente con los datos proporcionados
        self.assertEqual(self.producer.first_name, "Juan")
        self.assertEqual(self.producer.last_name, "Pérez")

    def test_producer_str_representation(self):
        # Comprobar que el método __str__ del modelo devuelve el nombre completo del productor
        self.assertEqual(str(self.producer), "Juan Pérez")

    def test_producer_email_validation(self):
         # Verificar que se lanza una ValidationError al intentar crear un productor con un email inválido
        with self.assertRaises(ValidationError):
            producer = Producer(
                identity_document="0987654321",
                first_name="María",
                last_name="García",
                phone="0987654321",
                email="invalid-email"
            )
            producer.full_clean()  # Esto forzará la validación

# Pruebas para el modelo Farm (Finca)
# Crear un productor y una finca de ejemplo para usar en las pruebas
class FarmTestCase(TestCase):
    def setUp(self):
        self.producer = Producer.objects.create(
            identity_document="1234567890",
            first_name="Juan",
            last_name="Pérez",
            phone="1234567890",
            email="juan@example.com"
        )
        self.farm = Farm.objects.create(
            producer=self.producer,
            cadastral_number="CAD123",
            municipality="Ciudad Ejemplo"
        )

    def test_farm_creation(self):
        # Verificar que la finca se crea correctamente con los datos proporcionados
        self.assertEqual(self.farm.cadastral_number, "CAD123")
        self.assertEqual(self.farm.municipality, "Ciudad Ejemplo")

    # Comprobar que la relación entre la finca y el productor se establece correctamente
    def test_farm_producer_relationship(self):
        self.assertEqual(self.farm.producer, self.producer)

    # Verificar que la relación inversa entre el productor y sus fincas funciona
    def test_producer_farms_relationship(self):
        self.assertEqual(self.producer.farms.first(), self.farm)

# Crear un productor, una finca y un vivero de ejemplo para usar en las pruebas
class NurseryTestCase(TestCase):
    def setUp(self):
        self.producer = Producer.objects.create(
            identity_document="1234567890",
            first_name="Juan",
            last_name="Pérez",
            phone="1234567890",
            email="juan@example.com"
        )
        self.farm = Farm.objects.create(
            producer=self.producer,
            cadastral_number="CAD123",
            municipality="Ciudad Ejemplo"
        )
        self.nursery = Nursery.objects.create(
            farm=self.farm,
            code="NUR001",
            crop_type="Tomates"
        )

    def test_nursery_creation(self):
        self.assertEqual(self.nursery.code, "NUR001")
        self.assertEqual(self.nursery.crop_type, "Tomates")

    # Comprobar que la relación entre el vivero y la finca se establece correctamente
    def test_nursery_farm_relationship(self):
        self.assertEqual(self.nursery.farm, self.farm)

    # Verificar que la relación inversa entre la finca y sus viveros funciona
    def test_farm_nurseries_relationship(self):
        self.assertEqual(self.farm.nurseries.first(), self.nursery)

# Crear todas las instancias necesarias para probar la aplicación de producto
class ProductApplicationTestCase(TestCase):
    def setUp(self):
        self.producer = Producer.objects.create(
            identity_document="1234567890",
            first_name="Juan",
            last_name="Pérez",
            phone="1234567890",
            email="juan@example.com"
        )
        self.farm = Farm.objects.create(
            producer=self.producer,
            cadastral_number="CAD123",
            municipality="Ciudad Ejemplo"
        )
        self.nursery = Nursery.objects.create(
            farm=self.farm,
            code="NUR001",
            crop_type="Tomates"
        )
        self.task = Task.objects.create(
            nursery=self.nursery,
            date=timezone.now().date(),
            description="Aplicación de fungicida"
        )
        self.fungus_control = FungusControl.objects.create(
            ica_registration="ICA123",
            name="Fungicida X",
            application_frequency=15,
            price=Decimal("50.00"),
            withdrawal_period=7,
            fungus_name="Hongo Y"
        )
        self.product_application = ProductApplication.objects.create(
            task=self.task,
            content_type=ContentType.objects.get_for_model(FungusControl),
            object_id=self.fungus_control.id,
            application_date=timezone.now().date()
        )

    def test_product_application_creation(self):
        self.assertIsNotNone(self.product_application.application_date)

    # Comprobar que la relación entre la aplicación de producto y la tarea se establece correctamente
    def test_product_application_task_relationship(self):
        self.assertEqual(self.product_application.task, self.task)

    def test_product_application_product_relationship(self):
        self.assertEqual(self.product_application.product, self.fungus_control)

    def test_task_product_applications_relationship(self):
        self.assertEqual(self.task.applications.first(), self.product_application)