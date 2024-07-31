from django.shortcuts import render
from .models import Project, ProjectPhase

def dashboard(request):
    project = Project.objects.first()  # Assuming we're displaying one project
    phases = ProjectPhase.objects.filter(project=project)
    
    context = {
        'project': project,
        'phases': phases,
    }
    return render(request, 'dashboard/dashboard.html', context)