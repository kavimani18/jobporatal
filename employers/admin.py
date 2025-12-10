from django.contrib import admin
from .models import JobPost

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'salary', 'location', 'created_at')
    search_fields = ('title', 'location', 'salary')
    list_filter = ('location', 'created_at')
    ordering = ('-created_at',)

admin.site.register(JobPost, JobPostAdmin)
