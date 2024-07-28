from flask import Flask, render_template



app = Flask(__name__)

@app.route('/')
def dashboard():
    # In a real application, you would fetch this data from a database or API
    data = {
        'total_budget': 93332,
        'actual_cost': 48048,
        'spi': 0.89,
        'cpi': 0.87,
        'planned_value': 46666.00,
        'earned_value': 41579.40,
        'time_vs_project_phase': {
            'Closure Stage': 5,
            'Execution Stage': 164,
            'Monitor & Control': 3,
            'Project Initiation Stage': 40,
            'Project Planning Stage': 144
        },
        'project_phase_completion': {
            'Project Planning Stage': 60.0,
            'Project Initiation Stage': 100.0,
            'Monitor & Control': 11.3,
            'Execution Stage': 0.3,
            'Closure Stage': 0.0
        }
    }
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)