from django.db import models
from django.db.models import Avg # ⚠️ IMPORTAÇÃO CRÍTICA

# =========================================================
# 1. MODELOS INDEPENDENTES (BASE)
# =========================================================

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
    
# =========================================================
# 2. MODELOS DEPENDENTES
# =========================================================

class Professor(models.Model):
    nome_completo = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11, unique=True)
    data_contratacao = models.DateField()
    area_especializacao = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    disciplinas = models.ManyToManyField(
        'Disciplina',
        related_name='professores',
        blank=True
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

    def __str__(self):
        return self.nome_completo

    # ✅ PROPRIEDADE OBRIGATÓRIA (Cálculo Global)
    @property
    def media_geral(self):
        """Calcula a média de todas as notas do aluno dinamicamente."""
        # Usa o ORM para calcular a média de todas as notas relacionadas
        agregacao = self.notas.aggregate(media=Avg('valor'))
        nova_media = agregacao.get('media')
        if nova_media is not None:
            return round(nova_media, 2)
        return 0.0

    # ✅ PROPRIEDADE OBRIGATÓRIA (Cálculo por Matéria)
    @property
    def medias_por_disciplina(self):
        """Retorna a média agrupada por nome da disciplina."""
        medias = self.notas.values('disciplina__nome').annotate(
            media_disciplina=Avg('valor')
        ).order_by('disciplina__nome')

        resultado = []
        for item in medias:
            media_arredondada = round(item['media_disciplina'], 2)
            resultado.append({
                'disciplina': item['disciplina__nome'],
                'media': media_arredondada
            })
        return resultado

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
        return f"{self.aluno.nome_completo} - Nota: {self.valor} - ({self.disciplina.nome})"