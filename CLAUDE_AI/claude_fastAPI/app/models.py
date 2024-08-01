from pydantic import BaseModel

class ProjectData(BaseModel):
    name: str = "IT Career map"
    phase: str = "2 selected"
    total_budget: float = 93332
    actual_cost: float = 48048
    spi: float = 0.89
    cpi: float = 0.87
    planned_value: float = 46666.00
    earned_value: float = 41579.40
    phase_hours: dict = {
        'Closure Stage': 5,
        'Execution Stage': 164,
        'Monitor & Control': 36,
        'Project Initiation Stage': 40,
        'Project Planning Stage': 144
    }
    phase_completion: dict = {
        'Project Planning Stage': 80.0,
        'Project Initiation Stage': 100.0,
        'Monitor & Control': 11.3,
        'Execution Stage': 8.0,
        'Closure Stage': 0.7
    }