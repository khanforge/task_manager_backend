from rest_framework import serializers
from projects.models import Project, Task
from users.models import User
from rest_framework.permissions import BasePermission

class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Project
        fields = "__all__"

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "role"]

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserBasicSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["project", "created_by"]

    def create(self, validated_data):
        project_id = self.context.get("project_id")
        created_by = self.context.get("created_by")

        return Task.objects.create(
            project_id=project_id,
            created_by=created_by,
            **validated_data
        )

    


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'