from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

task_list = TaskViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

task_detail = TaskViewSet.as_view({
    'patch': 'partial_update',
})

urlpatterns = [
    path("api/", include(router.urls)),

    path(
        "api/<int:project_id>/tasks/",
        task_list,
        name="project-tasks"
    ),
    path(
    "api/<int:project_id>/tasks/<int:pk>/",
    task_detail,
    name="project-task-detail"
),
]