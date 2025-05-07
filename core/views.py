# core/views.py
from rest_framework import viewsets
from .models import Paciente, HistoriaClinica
from .serializers import (
    PacienteSerializer,
    HistoriaClinicaSerializer,
    PacienteConHistoriaSerializer
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class HistoriaClinicaViewSet(viewsets.ModelViewSet):
    
    def get_queryset(self):
        qs = HistoriaClinica.objects.select_related('paciente').all()
        pid = self.request.query_params.get('paciente')
        if pid:
            try:
                qs = qs.filter(paciente_id=int(pid))
            except (ValueError, TypeError):
                return qs.none()
        return qs
    serializer_class = HistoriaClinicaSerializer
    filterset_fields = ['paciente']  # habilita ?paciente=<id> en la URL

@method_decorator(csrf_exempt, name='dispatch')
class PacienteViewSet(viewsets.ModelViewSet):
    queryset         = Paciente.objects.all()
    serializer_class = PacienteConHistoriaSerializer


