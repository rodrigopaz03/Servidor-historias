from rest_framework import viewsets
from .models import Paciente, HistoriaClinica
from .serializers import (
    PacienteSerializer,
    HistoriaClinicaSerializer,
    PacienteConHistoriaSerializer
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse

@method_decorator(csrf_exempt, name='dispatch')
class HistoriaClinicaViewSet(viewsets.ModelViewSet):
    queryset = HistoriaClinica.objects.select_related('paciente').all()
    serializer_class = HistoriaClinicaSerializer
    filterset_fields = ['paciente']

    def get_queryset(self):
        qs = self.queryset
        pid = self.request.query_params.get('paciente')

        if pid:
            try:
                pid = int(pid)  # Intentamos convertir a entero
                if pid <= 0:  # Validamos que el ID sea positivo
                    raise ValidationError("El ID del paciente debe ser un número entero positivo.")
                qs = qs.filter(paciente_id=pid)  # Usamos el ORM para evitar SQL manual
            except (ValueError, TypeError):
                return JsonResponse({"error": "ID de paciente no válido"}, status=400)

        return qs


@method_decorator(csrf_exempt, name='dispatch')
class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteConHistoriaSerializer

    def create(self, request, *args, **kwargs):
        """
        Sobrescribir el método de creación para validar más parámetros si es necesario
        y prevenir inyecciones.
        """
        try:
            identificacion = request.data.get('identificacion')
            if not identificacion.isdigit():
                raise ValidationError("La identificación solo puede contener números.")

            return super().create(request, *args, **kwargs)
        
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
