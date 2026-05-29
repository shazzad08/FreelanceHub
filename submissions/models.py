from django.db import models
from projects.models import Project
from accounts.models import User


class Submission(models.Model):

    project = models.OneToOneField(Project,on_delete=models.CASCADE)

    freelancer = models.ForeignKey(User,on_delete=models.CASCADE)

    message = models.TextField()

    file = models.FileField(upload_to='submissions/')

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.project.title