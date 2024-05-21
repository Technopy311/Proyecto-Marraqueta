from django.contrib.auth.models import AbstractUser
from django.db import models

""" Base User Models """

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADM", 'Admin'
        STUDENT = "STU", 'Student'
        PROFESSOR = "PRO", 'Professor'
        ACADEMIC = "ACA", 'Academic'
        EXTERNAL = "EXT", 'External'
        STAFF = "STA", 'Staff'
        GUARD = "GUA", 'Guard'

    is_guard = models.BooleanField("Es Guardia?", default=False)
    AbstractUser.username = models.CharField(verbose_name="Nombre", max_length=25, null=None)
    user_type = models.CharField(choices=Role.choices, default="STU", max_length=3)
    last_name = models.CharField(verbose_name="Apellido", max_length=25, null=None)
    run = models.PositiveBigIntegerField(
        verbose_name="RUN", 
        null=True, 
        unique=True, 
        error_messages={
            'unique': "Ese RUN ya se encuentra registrado."
        })
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.user_type
            return super().save(*args, **kwargs)

class UsmUser(User):
    AbstractUser.email = models.EmailField(
        verbose_name="Email USM", 
        max_length=25, 
        null=None, 
        unique=True,
        error_messages={
            'unique': "Ese correo ya se encuentra registrado."
        })
    usm_role = models.PositiveBigIntegerField(
        verbose_name="ROL USM", 
        null=True, 
        default=None,
        error_messages={
            'unique': "Ese ROL ya se encuentra regisrado."
        })

class OtherUser(User):
    AbstractUser.email = models.EmailField(
        verbose_name="Email", 
        max_length=25, 
        null=None, 
        unique=True,
        error_messages={
            'unique': "Ese correo ya se encuentra registrado."
        })


""" Derivative user models """

class Student(UsmUser):
    User.user_type = User.Role.STUDENT
    career = models.CharField("Carrera", max_length=20, default=None, null=True) #TODO CHANGE CAREER TO CHOICES FIELD

    def __str__(self):
        return "Estudiante " + str(self.run)
    
    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

class Professor(UsmUser):
    User.user_type = User.Role.PROFESSOR
    department = models.CharField("Departamento", max_length=20, default=None, null=True)
    
    def __str__(self):
        return "Profesor " + str(self.run)
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"

class Academic(OtherUser):
    User.user_type = User.Role.ACADEMIC
    connection = models.CharField("Conexión con USM", max_length=100, default=None, null=True)

    def __str__(self):
        return "Academico " + str(self.run)
    
    class Meta:
        verbose_name = "Academico"
        verbose_name_plural = "Academicos"

class External(OtherUser):
    User.user_type = User.Role.EXTERNAL
    connection = models.CharField("Conexión con USM", max_length=100, default=None, null=True)

    def __str__(self):
        return "Externo " + str(self.run)
    
    class Meta:
        verbose_name = "Externo"
        verbose_name_plural = "Externos"

class Staff(OtherUser):
    User.user_type = User.Role.STAFF
    charge = models.CharField("Cargo en USM", max_length=40, default=None, null=True)
    def __str__(self):
        return "Staff " + str(self.run)
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"

class Guard(OtherUser):
    User.is_guard = True
    def __str__(self):
        return "Guardia " + str(self.run)
    
    class Meta:
        verbose_name = "Guardia"
        verbose_name_plural = "Guardias"
    



""" Non Human Models """

class Bicycle(models.Model):
    BIKES_CHOICES = {
        "RB": "Road Bike",
        "CCB": "Cyclo-cross Bike",
        "GB": "Grave Bike",
        "TTB": "Time Trial Bike",
        "TB": "Touring Bike",
        "FB": "Folding Bike",
        "BMX": "BMX",
        "EB": "Electric Bike"
    }

    model = models.CharField("Bicycle model", max_length=100, null=False)
    colour = models.CharField("Bicycle color", max_length=100, null=False)
    bike_type = models.CharField(
        max_length=3,
        choices=BIKES_CHOICES,
        default="RB",
        null=False
    )
    bicy_user = models.ForeignKey("Student", on_delete=models.CASCADE)
    is_saved = models.BooleanField("Am I saved?", default=False)

    image = models.ImageField(upload_to="uploads/", default=None, null=True)

class KeyChain(models.Model):
    uuid = models.UUIDField(default=None, editable=True)
    user = models.ForeignKey("Student", on_delete=models.CASCADE)

class BicycleHolder(models.Model):
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        """
            This code below, adds or deletes BicycleHolder slots when saving the instance.
        """
        self_slots = self.tracker["slots"]
        if len(self_slots) == 0:
            for i in range(self.capacity):
                self_slots.append(0)
        else:
            delta_capacity = self.capacity - len(self_slots)
            if delta_capacity > 0:
                for i in range(delta_capacity):
                    self_slots.append(0)
            else:
                self_slots = self_slots[:self.capacity]
        
        print(f"{self.__str__} modified, slots: {self_slots}")

    def check_bicycle(self, bicycle):
        """Check if the given Bicycle is in the slots arr

        Args:
            Bicycle (core.models.Bicycle): _description_

        Returns:
            Int: not -1 if exists. -1 if not exists.
        """
        bicycle_pk = bicycle.pk
        self_slots = self.tracker['slots']

        try:
            return self_slots.index(bicycle_pk)
        except ValueError:
            return -1

    def add_bicycle(self, bicycle):
        """Add a bicycle instance's PK to the slots arr.

        Args:
            Bicycle (core.models.Bicycle): instance of core.Bicycle model.

        Returns:
            (Int, Int/None): Tuple(Status Code, Empty_Place's index). Status code: 0(success), 1(Bicycle not instance of Bicycle), 2(No empty place)
        """
        self_slots = self.tracker["slots"]
        if isinstance(bicycle, Bicycle): # check if bicycle belongs to Bicycleclass
            try:
                empty_place = self_slots.index(0)
                self_slots[empty_place] = bicycle.pk
                return (0, empty_place)
            except ValueError:
                return (2, None)
        else:
            return (1, None)

    def del_bicycle(self, bicycle):
        """Deletes a bicycle from the BicycleHolder

        Args:
            bicycle_pk (Int): The primary key of a core.Bicycle model

        Returns:
            Int: 0 deletion successful; 1 bicycle_pk not in slots
        """
        self_slots = self.tracker["slots"]
        bicycle_pk = bicycle.pk
        if type(bicycle_pk) == type(0):  # Check if the type of bicycle_pk is int
            try:
                bicycle_index = self_slots.index(bicycle_pk)
                self_slots[bicycle_index] = 0
                return 0
            except ValueError:
                return 1

    BUILDING_SJ_CHOICES = {
        "K": "K",
        "A": "A",
        "B": "B",
        "C": "C",
        "E": "E"
    }

    def get_default_json():
        print(type({"slots": []}))
        return {"slots": []}

    tracker = models.JSONField(default=get_default_json)
    capacity = models.PositiveSmallIntegerField("Capacity", default=1, null=False)
    location = models.CharField("Location", max_length=30)
    nearest_building = models.CharField("Nearest building", max_length=1, choices=BUILDING_SJ_CHOICES)
    nearest_guard = models.ForeignKey("Guard", on_delete=models.CASCADE, default=None, null=True)

class EspModule(models.Model):
    ip_address = models.GenericIPAddressField(protocol='IPv4', default=None, null=True)
    latest_online = models.DateTimeField("Lastest online", null=True)
    bicycleholder = models.OneToOneField(BicycleHolder, on_delete=models.CASCADE, default=None)
