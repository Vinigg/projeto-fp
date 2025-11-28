from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Turma, Disciplina, Professor, Aluno, Nota
# ⚠️ IMPORTAÇÃO CORRETA (SINGULAR)
from .serializers import (
    TurmaSerializer, 
    DisciplinaSerializer, 
    ProfessorSerializer, 
    AlunoSerializer, 
    NotaSerializer
)

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all().order_by('nome')
    serializer_class = TurmaSerializer

    @action(detail=True, methods=['get'])
    def alunos(self, request, pk=None):
        try:
            turma = Turma.objects.get(pk=pk)
        except Turma.DoesNotExist:
            return Response(status=404, data={"detail": "Turma não encontrada."})
        
        alunos = turma.alunos.all().order_by('nome_completo')
        serializer = AlunoSerializer(alunos, many=True)
        return Response(serializer.data)

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all().order_by('nome')
    serializer_class = DisciplinaSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all().order_by('nome_completo')
    serializer_class = ProfessorSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all().order_by('nome_completo')
    serializer_class = AlunoSerializer

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer