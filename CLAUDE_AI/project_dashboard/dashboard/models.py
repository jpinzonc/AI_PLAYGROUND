from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2)
    spi = models.FloatField()
    cpi = models.FloatField()
    planned_value = models.DecimalField(max_digits=10, decimal_places=2)
    earned_value = models.DecimalField(max_digits=10, decimal_places=2)

class ProjectPhase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hours = models.IntegerField()
    completion_percentage = models.FloatField()