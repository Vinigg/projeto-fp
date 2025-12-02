from django.shortcuts import render
from rest_framework import viewsets
from .models import Turma, Disciplina, Professor, Aluno, Nota
from .serializers import TurmaSerializer, DisciplinaSerializer, ProfessorSerializer, AlunosSerializer, NotaSerializer


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all().order_by('nome')
    serializer_class = TurmaSerializer

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all().order_by('nome')
    serializer_class = DisciplinaSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all().order_by('nome_completo')
    serializer_class = ProfessorSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all().order_by('nome_completo')
    serializer_class = AlunosSerializer

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

