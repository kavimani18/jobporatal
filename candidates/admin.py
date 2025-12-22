from django.contrib import admin
from .models import JobApplication


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job', 'applied_at')
    list_filter = ('applied_at', 'job')
    search_fields = ('name', 'email', 'job__title')

admin.site.register(JobApplication,JobApplicationAdmin)