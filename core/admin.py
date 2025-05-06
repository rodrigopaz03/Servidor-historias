from django.contrib import admin
from .models import Paciente, HistoriaClinica

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display  = ("identificacion", "nombre", "apellido", "fecha_nacimiento")
    search_fields = ("identificacion", "nombre", "apellido")

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display  = ("id", "paciente", "fecha_apertura", "medico_responsable")
    list_filter   = ("medico_responsable",)
    search_fields = ("paciente__identificacion", "paciente__nombre", "paciente__apellido")


