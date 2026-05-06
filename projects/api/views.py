from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from projects.models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

class DashboardView(APIView):
    def get(self, request):
        user = request.user

        tasks = Task.objects.filter(assigned_to=user)

        data = {
            "total": tasks.count(),
            "completed": tasks.filter(status='done').count(),
            "in_progress": tasks.filter(status='in_progress').count(),
            "overdue": tasks.filter(due_date__lt=now(), status__in=['todo', 'in_progress']).count(),
        }

        return Response(data)

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()  
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(created_by=self.request.user)
        # project.members.add(self.request.user)

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        if not project_id:
            return Task.objects.none()
        return Task.objects.filter(project_id = project_id)

    def create(self, request, *args, **kwargs):
        project_id = kwargs.get("project_id")
        print(request.data, " ", project_id)
        serializer = TaskSerializer(
            data=request.data,
            context = {
                "project_id":project_id,
                "created_by":self.request.user
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    # def perform_create(self, serializer):
    #     project_id = self.kwargs.get("project_id")
    #     # if self.request.user.role != 'admin':
    #     #     raise PermissionDenied("Only admin can create tasks")

    #     serializer.save(
    #         project_id=project_id,
    #         created_by=self.request.user
    #     )