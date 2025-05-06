# core/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    PacienteViewSet,
    HistoriaClinicaViewSet,
)

router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet)
router.register(r'historias', HistoriaClinicaViewSet)

urlpatterns = router.urls

