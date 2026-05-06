from django.db import models
from users.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_projects"
    )
    # members = models.forei(User, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks"
    )

    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tasks"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')

    due_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)