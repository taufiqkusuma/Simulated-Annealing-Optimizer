from flask import Flask, render_template, request, jsonify
from simulated_annealing import simulated_annealing, calculate_cost

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_simulation():
    data = request.json
    flow_matrix = data['flow_matrix']
    dept_sizes = data['dept_sizes']
    area_size = data['area_size']
    T_init = data['T_init']
    cooling_rate = data['cooling_rate']
    max_iter = data['max_iter']

    best_layout, best_cost = simulated_annealing(flow_matrix, dept_sizes, area_size, T_init, cooling_rate, max_iter)

    return jsonify({
        'best_layout': best_layout.tolist(),
        'best_cost': best_cost
    })

if __name__ == '__main__':
    app.run(debug=True)
