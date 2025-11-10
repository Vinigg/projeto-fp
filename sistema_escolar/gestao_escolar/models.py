from django.db import models

# Create your models here.

# Modelo para turmas e materias

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.IntegerField()

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self):
        return f"{self.nome} - {self.ano}"
    
class Disciplina(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    
# Modelos com depêndencia 

class Professor(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11, unique=True)
    data_contratacao = models.DateField()
    area_especializacao = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    turma_responsavel = models.ForeignKey(
        Turma,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='professor_responsavel'
    )

    def __str__(self):
        return self.nome_completo
    
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

    media_geral = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

    def __str__(self):
        return self.nome_completo

class Nota(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name='notas'
    )

    disciplina = models.ForeignKey(
        Disciplina,
        on_delete=models.PROTECT,
    )

    valor = models.DecimalField(max_digits=4, decimal_places=2)
    data_avaliacao = models.DateField()

    def __str__(self):
        return f"{self.aluno.nome_completo} - Nota: {self.valor} - ({self.desciplina.nome})"