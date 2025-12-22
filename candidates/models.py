from django.contrib.auth.models import User
from django.db import models

class JobApplication(models.Model):
    job = models.ForeignKey('employers.JobPost', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Required - securely links to candidate account
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    resume = models.FileField(upload_to='media/resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.name} - {self.job.title}"
