from rest_framework import serializers
from django.db import transaction
from datetime import date 
from .models import Turma, Disciplina, Professor, Aluno, Nota, TurmaDisciplina

class TurmaDisciplinaSerializer(serializers.ModelSerializer):
    disciplina_nome = serializers.CharField(source='disciplina.nome', read_only=True)
    professor_nome = serializers.CharField(source='professor.nome_completo', read_only=True)

    class Meta:
        model = TurmaDisciplina
        fields = ['id', 'disciplina', 'disciplina_nome', 'professor', 'professor_nome']

class TurmaSerializer(serializers.ModelSerializer):
    grade = TurmaDisciplinaSerializer(many=True, read_only=True)
    
    grade_dados = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Turma
        fields = ['id', 'nome', 'ano', 'grade', 'grade_dados']

    def create(self, validated_data):
        grade_dados = validated_data.pop('grade_dados', [])
        
        with transaction.atomic():
            turma = Turma.objects.create(**validated_data)
            
            for item in grade_dados:
                TurmaDisciplina.objects.create(
                    turma=turma, 
                    disciplina_id=item['disciplina'], 
                    professor_id=item['professor']
                )
            
        return turma

    def update(self, instance, validated_data):
        grade_dados = validated_data.pop('grade_dados', None)
        
        with transaction.atomic():
            instance.nome = validated_data.get('nome', instance.nome)
            instance.ano = validated_data.get('ano', instance.ano)
            instance.save()

            if grade_dados is not None:
                instance.grade.all().delete()
                
                for item in grade_dados:
                    TurmaDisciplina.objects.create(
                        turma=instance, 
                        disciplina_id=item['disciplina'], 
                        professor_id=item['professor']
                    )
        
        return instance

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

    def validate(self, data):
        dt_nasc = data.get('data_nascimento')
        dt_contr = data.get('data_contratacao')
        hoje = date.today() 

        if dt_nasc and dt_nasc > hoje:
            raise serializers.ValidationError({"data_nascimento": "A data de nascimento não pode estar no futuro."})
        
        if dt_contr and dt_contr > hoje:
            raise serializers.ValidationError({"data_contratacao": "A data de contratação não pode estar no futuro."})

        
        if dt_nasc and dt_contr:
            
            idade_na_contratacao = dt_contr.year - dt_nasc.year - ((dt_contr.month, dt_contr.day) < (dt_nasc.month, dt_nasc.day))
            
            if idade_na_contratacao < 18:
                raise serializers.ValidationError({
                    "data_contratacao": f"Professor deve ter no mínimo 18 anos na data da contratação. Idade calculada: {idade_na_contratacao} anos."
                })
        
        return data

class AlunosSerializer(serializers.ModelSerializer):
    media_geral = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Aluno
        fields = '__all__'
    
    def validate_data_nascimento(self, value):
        if value > date.today():
            raise serializers.ValidationError("A data de nascimento não pode ser maior que o dia atual.")
        return value

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'
    
    def validate_valor(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("A nota deve estar entre 0 e 10")
        return value

    def validate(self, data):
        if self.instance:
            aluno = data.get('aluno', self.instance.aluno)
            disciplina = data.get('disciplina', self.instance.disciplina)
        else:
            aluno = data.get('aluno')
            disciplina = data.get('disciplina')

        if aluno and disciplina:
            
            existe_na_grade = TurmaDisciplina.objects.filter(
                turma=aluno.turma,
                disciplina=disciplina
            ).exists()

            if not existe_na_grade:
                raise serializers.ValidationError({
                    "disciplina": f"O aluno {aluno.nome_completo} (Turma: {aluno.turma.nome}) não cursa a disciplina {disciplina.nome}."
                })

        return data