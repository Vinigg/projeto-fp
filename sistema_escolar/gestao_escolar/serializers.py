from rest_framework import serializers
from .models import Turma, Disciplina, Professor, Aluno, Nota

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

class AlunosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'
    
    def validate_valor(self, value):
        """Valida se a nota está entre 0 e 10"""
        if value < 0 or value > 10:
            raise serializers.ValidationError("A nota deve estar entre 0 e 10")
        return value

