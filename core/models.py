from django.db import models

class Paciente(models.Model):
    identificacion     = models.CharField("ID paciente", max_length=50, unique=True)
    nombre             = models.CharField("Nombre", max_length=100)
    apellido           = models.CharField("Apellido", max_length=100)
    fecha_nacimiento   = models.DateField("Fecha de nacimiento")
    sexo               = models.CharField(
                           "Sexo",
                           max_length=1,
                           choices=[("M","Masculino"),("F","Femenino")]
                        )
    telefono           = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    email              = models.EmailField("Correo electrónico", blank=True, null=True)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.identificacion})"


class HistoriaClinica(models.Model):
    paciente           = models.ForeignKey(
                            Paciente,
                            related_name="historias",
                            on_delete=models.CASCADE
                        )
    fecha_apertura     = models.DateTimeField(auto_now_add=True)
    descripcion        = models.TextField("Motivo de consulta / notas iniciales")
    medico_responsable = models.CharField("Médico responsable", max_length=100)
    updated_by         = models.CharField("Actualizado por", max_length=100, blank=True, null=True)
    updated_at         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Historia #{self.id} - {self.paciente}"



