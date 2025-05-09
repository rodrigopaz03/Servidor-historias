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
import re

@method_decorator(csrf_exempt, name='dispatch')
class HistoriaClinicaViewSet(viewsets.ModelViewSet):
    queryset = HistoriaClinica.objects.select_related('paciente').all()
    serializer_class = HistoriaClinicaSerializer
    filterset_fields = ['paciente']

    def validate_sql_injection(self, input_value):
        """
        Función que valida la entrada para prevenir inyecciones SQL.
        """
        # Regex para detectar patrones de inyección SQL comunes
        sql_injection_patterns = [r'--', r'\'', r'\"', r'OR', r'AND', r'1=1', r'UNION', r'SELECT', r'INSERT']
        for pattern in sql_injection_patterns:
            if re.search(pattern, input_value, re.IGNORECASE):
                raise ValidationError(f"Entrada maliciosa detectada: {input_value}")

    def get_queryset(self):
        qs = self.queryset
        pid = self.request.query_params.get('paciente')

        if pid:
            # Validamos la entrada para evitar inyecciones SQL
            self.validate_sql_injection(pid)
            try:
                pid = int(pid)  # Asegurarse de que el ID sea un número
                if pid <= 0:  # El ID debe ser positivo
                    raise ValidationError("El ID del paciente debe ser un número entero positivo.")
                qs = qs.filter(paciente_id=pid)  # Filtramos por ID de paciente
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
            
            # Validación de identificación para asegurarse de que solo contenga números
            if not identificacion.isdigit():
                raise ValidationError("La identificación solo puede contener números.")
            
            # Llamamos al método original de creación si la validación es exitosa
            return super().create(request, *args, **kwargs)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
