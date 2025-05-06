# core/views.py
from rest_framework import viewsets
from .models import Paciente, HistoriaClinica
from .serializers import (
    PacienteSerializer,
    HistoriaClinicaSerializer,
)

class PacienteViewSet(viewsets.ModelViewSet):
    queryset         = Paciente.objects.all()
    serializer_class = PacienteSerializer


class HistoriaClinicaViewSet(viewsets.ModelViewSet):
    queryset         = HistoriaClinica.objects.select_related('paciente').all()
    serializer_class = HistoriaClinicaSerializer
    filterset_fields = ['paciente']  # habilita ?paciente=<id> en la URL


