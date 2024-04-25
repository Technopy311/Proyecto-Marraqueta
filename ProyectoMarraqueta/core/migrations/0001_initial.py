# Generated by Django 5.0.3 on 2024-04-25 01:16

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[
                            ("ADM", "Admin"),
                            ("STU", "Student"),
                            ("PRO", "Professor"),
                            ("ACA", "Academic"),
                            ("EXT", "External"),
                            ("STA", "Staff"),
                            ("GUA", "Guard"),
                        ],
                        default="STU",
                        max_length=3,
                    ),
                ),
                (
                    "last_name",
                    models.CharField(max_length=25, null=None, verbose_name="Apellido"),
                ),
                (
                    "run",
                    models.PositiveBigIntegerField(
                        error_messages={
                            "unique": "Ese RUN ya se encuentra registrado."
                        },
                        null=None,
                        unique=True,
                        verbose_name="RUN",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="OtherUser",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="UsmUser",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "usm_role",
                    models.PositiveBigIntegerField(
                        default=None,
                        error_messages={"unique": "Ese ROL ya se encuentra regisrado."},
                        null=True,
                        verbose_name="ROL USM",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.user",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Academic",
            fields=[
                (
                    "otheruser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.otheruser",
                    ),
                ),
                (
                    "connection",
                    models.CharField(
                        default=None, max_length=100, verbose_name="Conexión con USM"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.otheruser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="External",
            fields=[
                (
                    "otheruser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.otheruser",
                    ),
                ),
                (
                    "connection",
                    models.CharField(
                        default=None, max_length=100, verbose_name="Conexión con USM"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.otheruser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Guard",
            fields=[
                (
                    "otheruser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.otheruser",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.otheruser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "otheruser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.otheruser",
                    ),
                ),
                (
                    "charge",
                    models.CharField(
                        default=None, max_length=40, verbose_name="Cargo en USM"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.otheruser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Professor",
            fields=[
                (
                    "usmuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.usmuser",
                    ),
                ),
                (
                    "department",
                    models.CharField(
                        default=None, max_length=20, verbose_name="Departamento"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.usmuser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "usmuser_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.usmuser",
                    ),
                ),
                (
                    "career",
                    models.CharField(
                        default=None, max_length=20, verbose_name="Carrera"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            bases=("core.usmuser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="BicycleHolder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "capacity",
                    models.PositiveSmallIntegerField(
                        default=1, verbose_name="Capacity"
                    ),
                ),
                ("location", models.CharField(max_length=30, verbose_name="Location")),
                (
                    "nearest_building",
                    models.CharField(
                        choices=[
                            ("K", "K"),
                            ("A", "A"),
                            ("B", "B"),
                            ("C", "C"),
                            ("E", "E"),
                        ],
                        max_length=1,
                        verbose_name="Nearest building",
                    ),
                ),
                (
                    "nearest_guard",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.guard",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="KeyChain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.PositiveBigIntegerField(
                        default=None, null=True, verbose_name="UUID"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.student"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bicycle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "model",
                    models.CharField(max_length=100, verbose_name="Bicycle model"),
                ),
                (
                    "colour",
                    models.CharField(max_length=100, verbose_name="Bicycle color"),
                ),
                (
                    "bike_type",
                    models.CharField(
                        choices=[
                            ("RB", "Road Bike"),
                            ("CCB", "Cyclo-cross Bike"),
                            ("GB", "Grave Bike"),
                            ("TTB", "Time Trial Bike"),
                            ("TB", "Touring Bike"),
                            ("FB", "Folding Bike"),
                            ("BMX", "BMX"),
                            ("EB", "Electric Bike"),
                        ],
                        default="RB",
                        max_length=3,
                    ),
                ),
                (
                    "bicy_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.student"
                    ),
                ),
            ],
        ),
    ]
