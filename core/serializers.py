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
    id = serializers.ReadOnlyField()   # <— lo añades aquí
    historia_inicial = serializers.DictField(
        write_only=True, required=False,
        help_text="(Opcional) descripcion y medico_responsable"
    )

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
        # Si viniera algo, lo extraemos; sino, queda {}
        historia_data = validated_data.pop('historia_inicial', {}) or {}
        # 1) Creamos el paciente
        paciente = Paciente.objects.create(**validated_data)
        # 2) Creamos siempre la historia, con valores por defecto si no vienen
        HistoriaClinica.objects.create(
            paciente=paciente,
            descripcion=historia_data.get('descripcion', ''),
            medico_responsable=historia_data.get('medico_responsable', '')
        )
        return paciente

class PacienteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
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
            # cualquier otro campo que tengas…
        ]

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

