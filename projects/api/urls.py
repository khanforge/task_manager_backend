from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

task_list = TaskViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path("api/", include(router.urls)),

    path(
        "api/<int:project_id>/tasks/",
        task_list,
        name="project-tasks"
    ),
]