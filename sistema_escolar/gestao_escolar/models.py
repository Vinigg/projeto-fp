from django.db import models
from django.core.exceptions import ValidationError


class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return self.nome

class Professor(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField(null=True, blank=True) 
    data_contratacao = models.DateField()
    area_especializacao = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    disciplinas = models.ManyToManyField(
        'Disciplina',
        related_name='professores',
        help_text='Disciplinas que o professor está apto a lecionar'
    )

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.nome_completo

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.IntegerField()

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self):
        return f"{self.nome} - {self.ano}"

class TurmaDisciplina(models.Model):

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='grade')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Grade Curricular"
        verbose_name_plural = "Grades Curriculares"
        unique_together = ['turma', 'disciplina']

    def __str__(self):
        return f"{self.turma} - {self.disciplina} ({self.professor})"

class Aluno(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11, unique=True)
    data_nascimento = models.DateField()
    data_matricula = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Ativo')

    turma = models.ForeignKey(
        Turma,
        on_delete=models.PROTECT,
        related_name='alunos'
    )

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return self.nome_completo
    
    @property
    def media_geral(self):
        from django.db.models import Avg
        resultado = self.notas.aggregate(Avg('valor'))
        return resultado['valor__avg'] or 0.0
    
    def media_por_disciplina(self):
        from django.db.models import Avg
        return self.notas.values('disciplina__nome').annotate(media=Avg('valor'))

class Nota(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name='notas'
    )

    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.PROTECT,
        related_name='notas'
    )

    valor = models.DecimalField(max_digits=4, decimal_places=2)
    data_avaliacao = models.DateField()

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        unique_together = [['aluno', 'disciplina', 'data_avaliacao']]

    def __str__(self):
        return f"{self.aluno.nome_completo} - Nota: {self.valor} - ({self.disciplina.nome})"