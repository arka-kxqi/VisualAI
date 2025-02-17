from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    USER_ROLES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    profile_picture = models.ImageField(null=True, blank=True)
    birth=models.DateField(null=True)
    specialization=models.CharField(null=True,max_length=50)
    education=models.TextField(null=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class TemporaryLabReport(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='lab_reports')
    ocr_text = models.TextField(null=True, blank=True)
    gemini_prompt1_response = models.TextField(null=True, blank=True)
    original_report_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ocr_confidence = models.TextField(null=True, blank=True)
    address_of_hospital = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='temp_lab_img', null=True)


class Test(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tests')
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class LabReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    test_name = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='lab_reports', null=True)
    sample = models.CharField(max_length=200, null=True, blank=True)
    report_data = models.JSONField()
    report_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ocr_conf = models.TextField(null=True, blank=True)
    hospital_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Lab Report  for {self.test_name} by {self.user.username} on {self.report_date}"


class LabReportImage(models.Model):
    lab_report = models.ForeignKey(
        LabReport, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='lab_reports')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField()

    def __str__(self):
        return f"Image {self.id} for Lab Report {self.lab_report.id}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    )

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField(null=True)
    apointment_time = models.TimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    meeting_id = models.CharField(max_length=100, blank=True, null=True)
    join_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Appointment on {self.appointment_date} with Dr. {self.doctor.username} id {self.id}"

    class Meta:
        indexes = [
            models.Index(fields=['patient', 'doctor', 'appointment_date']),
        ]


class ZoomToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField(null=True)
    refresh_token = models.TextField(null=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"ZoomToken for {self.user.username}"
