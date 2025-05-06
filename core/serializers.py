# core/serializers.py
from rest_framework import serializers
from .models import Paciente, HistoriaClinica

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Paciente
        fields = '__all__'


class HistoriaClinicaSerializer(serializers.ModelSerializer):
    # para mostrar el detalle del paciente al leer
    paciente = PacienteSerializer(read_only=True)
    # para asignar paciente al crear/actualizar por su ID
    paciente_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='paciente',
        queryset=Paciente.objects.all()
    )

    class Meta:
        model  = HistoriaClinica
        fields = [
            'id', 'paciente', 'paciente_id',
            'fecha_apertura', 'descripcion',
            'medico_responsable', 'updated_by', 'updated_at'
        ]


