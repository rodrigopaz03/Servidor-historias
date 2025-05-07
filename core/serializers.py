from rest_framework import serializers
from .models import Paciente, HistoriaClinica
from django.db import IntegrityError


class HistoriaInicialSerializer(serializers.ModelSerializer):
    """
    Serializer para los datos iniciales de HistoriaClínica al crear un paciente.
    """
    class Meta:
        model  = HistoriaClinica
        fields = ('descripcion', 'medico_responsable')

class PacienteConHistoriaSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()  
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
        historia_data = validated_data.pop('historia_inicial', {}) or {}

        try:
            paciente = Paciente.objects.create(**validated_data)
            
            HistoriaClinica.objects.create(
                paciente=paciente,
                descripcion=historia_data.get('descripcion', ''),
                medico_responsable=historia_data.get('medico_responsable', '')
            )
            
        except IntegrityError as e:
            raise serializers.ValidationError(f"Error al guardar el paciente: {str(e)}")
        except Exception as e:
            raise serializers.ValidationError(f"Ocurrió un error inesperado al guardar el paciente: {str(e)}")

        if not paciente.id:
            raise serializers.ValidationError("No se pudo guardar el paciente correctamente.")

        return paciente
    
    def validate_email(self, value):
        allowed_domains = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
        
        domain = value.split('@')[-1]
        
        if domain not in allowed_domains:
            raise serializers.ValidationError(f"El correo electrónico debe terminar en uno de los siguientes dominios: {', '.join(allowed_domains)}.")
        
        return value
    
    def validate_telefono(self, value):
        value = ''.join(filter(str.isdigit, value))
        
        if len(value) != 10:
            raise serializers.ValidationError("El número de teléfono debe tener exactamente 10 dígitos.")
        
        return value
    
    def update(self, instance, validated_data):
        historia_data = validated_data.pop('historia_inicial', {}) or {}

        try:
            instance.identificacion = validated_data.get('identificacion', instance.identificacion)
            instance.nombre = validated_data.get('nombre', instance.nombre)
            instance.apellido = validated_data.get('apellido', instance.apellido)
            instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
            instance.sexo = validated_data.get('sexo', instance.sexo)
            instance.telefono = validated_data.get('telefono', instance.telefono)
            instance.email = validated_data.get('email', instance.email)

            instance.save()

            historia_clinica = HistoriaClinica.objects.get(paciente=instance)
            historia_clinica.descripcion = historia_data.get('descripcion', historia_clinica.descripcion)
            historia_clinica.medico_responsable = historia_data.get('medico_responsable', historia_clinica.medico_responsable)
            historia_clinica.save()

        except IntegrityError as e:
            raise serializers.ValidationError(f"Error de integridad: {str(e)}")
        except HistoriaClinica.DoesNotExist:
            raise serializers.ValidationError("No se encontró la historia clínica del paciente.")
        except Exception as e:
            raise serializers.ValidationError(f"Error inesperado al actualizar el paciente: {str(e)}")

        return instance

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

