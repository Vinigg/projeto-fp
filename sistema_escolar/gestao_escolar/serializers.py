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
        moedl = Nota
        fields = '__all__'

