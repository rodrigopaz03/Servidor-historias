from rest_framework import serializers
from .models import Paciente, HistoriaClinica

class HistoriaInicialSerializer(serializers.ModelSerializer):
    """
    Serializer para los datos iniciales de HistoriaClínica al crear un paciente.
    """
    class Meta:
        model  = HistoriaClinica
        fields = ('descripcion', 'medico_responsable')

class PacienteConHistoriaSerializer(serializers.ModelSerializer):
    """
    Serializer que permite crear un Paciente y su HistoriaClínica inicial en una sola llamada.
    """
    historia_inicial = HistoriaInicialSerializer(write_only=True)

    class Meta:
        model  = Paciente
        fields = [
            'id',
            'identificacion',
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'sexo',
            'telefono',
            'email',
            'historia_inicial',
        ]

    def create(self, validated_data):
        # Extraemos los datos de la historia
        historia_data = validated_data.pop('historia_inicial')
        # Creamos el paciente
        paciente = Paciente.objects.create(**validated_data)
        # Asociamos la historia inicial
        HistoriaClinica.objects.create(
            paciente=paciente,
            **historia_data
        )
        return paciente

class PacienteSerializer(serializers.ModelSerializer):
    """
    Serializer básico para representar datos de Paciente.
    """
    class Meta:
        model  = Paciente
        fields = '__all__'

class HistoriaClinicaSerializer(serializers.ModelSerializer):
    """
    Serializer para CRUD de HistoriaClínica, mostrando datos anidados del paciente.
    """
    paciente    = PacienteSerializer(read_only=True)
    paciente_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='paciente',
        queryset=Paciente.objects.all()
    )

    class Meta:
        model  = HistoriaClinica
        fields = [
            'id',
            'paciente',
            'paciente_id',
            'fecha_apertura',
            'descripcion',
            'medico_responsable',
            'updated_by',
            'updated_at',
        ]

