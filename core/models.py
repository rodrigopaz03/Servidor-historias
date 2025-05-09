from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Paciente(models.Model):
    identificacion = models.CharField("ID paciente", max_length=50, unique=True)
    nombre = models.CharField("Nombre", max_length=100)
    apellido = models.CharField("Apellido", max_length=100)
    fecha_nacimiento = models.DateField("Fecha de nacimiento")
    sexo = models.CharField(
        "Sexo", max_length=1, choices=[("M", "Masculino"), ("F", "Femenino")]
    )
    telefono = models.CharField(
        "Teléfono", 
        max_length=20, 
        blank=True, 
        null=True, 
        validators=[RegexValidator(regex=r'^\d{10}$', message='El número debe tener 10 dígitos.')]
    )
    email = models.EmailField("Correo electrónico", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add set here
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Validación adicional para el correo electrónico
        allowed_domains = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
        if self.email:
            domain = self.email.split('@')[-1]
            if domain not in allowed_domains:
                raise ValidationError(f"El correo electrónico debe ser de uno de los siguientes dominios: {', '.join(allowed_domains)}")

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.identificacion})"


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(
        Paciente,
        related_name="historias",
        on_delete=models.CASCADE
    )
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField("Motivo de consulta / notas iniciales")
    medico_responsable = models.CharField("Médico responsable", max_length=100)
    updated_by = models.CharField("Actualizado por", max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.medico_responsable:
            if not self.medico_responsable.replace(' ', '').isalpha():
                raise ValidationError("El nombre del médico responsable debe contener solo letras y espacios.")

    def __str__(self):
        return f"Historia #{self.id} - {self.paciente}"

