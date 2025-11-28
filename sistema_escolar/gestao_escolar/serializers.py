from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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
    # O campo turma_responsavel foi removido do fields = '__all__'
    # O novo campo disciplina_principal será incluído automaticamente
    class Meta:
        model = Professor
        fields = '__all__' # Inclui todos os campos, incluindo a nova FK

class AlunoSerializer(serializers.ModelSerializer):
# ... (mantido o código de cálculo)
    media_geral = serializers.SerializerMethodField()
    medias_por_disciplina = serializers.SerializerMethodField()

    class Meta:
        model = Aluno
        fields = [
            'id', 'nome_completo', 'cpf', 'data_nascimento', 
            'data_matricula', 'status', 'turma', 
            'media_geral', 'medias_por_disciplina'
        ]

    def get_media_geral(self, obj):
        return obj.media_geral if obj.media_geral is not None else 0.0

    def get_medias_por_disciplina(self, obj):
        return obj.medias_por_disciplina

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'
        
    def validate_valor(self, valor):
        if valor < 0 or valor > 10.0:
            raise ValidationError("A nota deve estar entre 0 e 10.")
        return valor