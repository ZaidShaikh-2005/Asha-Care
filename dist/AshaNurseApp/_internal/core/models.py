from django.db import models


class Family(models.Model):
    family_name = models.CharField(max_length=100)

    village = models.ForeignKey(
        'Village',
        on_delete=models.PROTECT,
        related_name='families'
    )

    house_number = models.PositiveIntegerField()

    family_number = models.CharField(
        max_length=50,
        blank=True
    )

    contact_number = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(blank=True)

    area = models.CharField(
        max_length=100,
        blank=True
    )

    pin_code = models.CharField(
        max_length=10,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.family_name


class Member(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    RELATION_CHOICES = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Husband', 'Husband'),
        ('Wife', 'Wife'),
        ('Grandfather', 'Grandfather'),
        ('Grandmother', 'Grandmother'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Alive', 'Alive'),
        ('Dead', 'Dead'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('Unknown', 'Unknown'),
    ]

    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        related_name='members'
    )

    name = models.CharField(max_length=100)

    profile_photo = models.FileField(
        upload_to='profile_photos/',
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    blood_group = models.CharField(
        max_length=10,
        choices=BLOOD_GROUP_CHOICES,
        default='Unknown'
    )

    relation = models.CharField(
        max_length=20,
        choices=RELATION_CHOICES
    )

    currently_pregnant = models.BooleanField(
        default=False
    )

    pregnancy_start_date = models.DateField(
        blank=True,
        null=True
    )

    expected_delivery_date = models.DateField(
        blank=True,
        null=True
    )

    pregnancy_alert_sent = models.BooleanField(
        default=False
    )

    date_of_birth = models.DateField()

    religion = models.CharField(
        max_length=100
    )

    caste = models.CharField(
        max_length=150
    )

    bpl = models.BooleanField(
        default=False
    )

    mobile_number = models.CharField(
        max_length=15
    )

    bpl_number = models.CharField(
        max_length=100,
        blank=True
    )

    ayushman_card_number = models.CharField(
        max_length=100,
        blank=True
    )

    aadhaar_number = models.CharField(
        max_length=12
    )

    abha_number = models.CharField(
        max_length=100,
        blank=True
    )

    ayushman_card_file = models.FileField(
        upload_to='documents/ayushman/',
        blank=True,
        null=True
    )

    aadhaar_card_file = models.FileField(
        upload_to='documents/aadhaar/',
        blank=True,
        null=True
    )

    abha_card_file = models.FileField(
        upload_to='documents/abha/',
        blank=True,
        null=True
    )

    disease = models.TextField(
        blank=True
    )

    alive_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Alive'
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Village(models.Model):
    village_number = models.PositiveIntegerField(
        unique=True
    )

    name = models.CharField(
        max_length=200
    )

    total_houses = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.village_number} - {self.name}"