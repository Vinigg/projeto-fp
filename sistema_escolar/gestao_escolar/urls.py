from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TurmaViewSet, DisciplinaViewSet, ProfessorViewSet, AlunoViewSet, NotaViewSet


router = DefaultRouter()
router.register(r'turmas', TurmaViewSet)
router.register(r'disciplinas', DisciplinaViewSet)
router.register(r'professores', ProfessorViewSet)
router.register(r'alunos', AlunoViewSet)
router.register(r'notas', NotaViewSet)

urlpatterns = [
    path('', include(router.urls))
]

