import numpy as np
import random
import math

# Simulated Annealing Algorithm
def simulated_annealing(flow_matrix, dept_sizes, area_size, T_init, cooling_rate, max_iter):
    """
    Simulated Annealing Algorithm for facility layout optimization.

    Parameters:
        flow_matrix (list of list of int): Matrix representing flow between departments.
        dept_sizes (list of tuple): Sizes of departments (width, height).
        area_size (tuple): Total area size (width, height).
        T_init (float): Initial temperature.
        cooling_rate (float): Cooling rate.
        max_iter (int): Maximum number of iterations.

    Returns:
        best_layout (list): Optimal layout of departments.
        best_cost (float): Minimum cost of the layout.
    """
    num_depts = len(dept_sizes)
    layout = np.random.permutation(num_depts)  # Random initial solution
    best_layout = layout.copy()
    current_cost = calculate_cost(layout, flow_matrix, dept_sizes, area_size)
    best_cost = current_cost

    T = T_init

    for iteration in range(max_iter):
        # Generate a neighbor by swapping two departments
        new_layout = layout.copy()
        i, j = random.sample(range(num_depts), 2)
        new_layout[i], new_layout[j] = new_layout[j], new_layout[i]

        # Calculate the cost of the new layout
        new_cost = calculate_cost(new_layout, flow_matrix, dept_sizes, area_size)

        # Acceptance probability
        delta_cost = new_cost - current_cost
        if delta_cost < 0 or random.random() < math.exp(-delta_cost / T):
            layout = new_layout.copy()
            current_cost = new_cost

            # Update the best solution
            if current_cost < best_cost:
                best_layout = layout.copy()
                best_cost = current_cost

        # Cool down
        T *= cooling_rate

        # Stop if the temperature is very low
        if T < 1e-5:
            break

    return best_layout, best_cost


# Cost Calculation Function
def calculate_cost(layout, flow_matrix, dept_sizes, area_size):
    """
    Calculate the total cost of a given layout based on distances and flow.

    Parameters:
        layout (list): Layout of departments.
        flow_matrix (list of list of int): Matrix representing flow between departments.
        dept_sizes (list of tuple): Sizes of departments (width, height).
        area_size (tuple): Total area size (width, height).

    Returns:
        total_cost (float): Total cost of the layout.
    """
    num_depts = len(dept_sizes)
    positions = assign_positions(layout, dept_sizes, area_size)
    total_cost = 0

    for i in range(num_depts):
        for j in range(num_depts):
            if i != j:
                # Calculate Euclidean distance between departments
                dist = np.linalg.norm(np.array(positions[i]) - np.array(positions[j]))
                total_cost += flow_matrix[i][j] * dist

    return total_cost


# Assign Positions Based on Layout
def assign_positions(layout, dept_sizes, area_size):
    """
    Assign positions to departments based on their layout.

    Parameters:
        layout (list): Layout of departments.
        dept_sizes (list of tuple): Sizes of departments (width, height).
        area_size (tuple): Total area size (width, height).

    Returns:
        positions (list of tuple): Positions of departments.
    """
    positions = []
    current_x, current_y = 0, 0

    for dept in layout:
        width, height = dept_sizes[dept]
        # Position is the center of the department
        positions.append((current_x + width / 2, current_y + height / 2))
        current_x += width

        # Move to the next row if width exceeds area size
        if current_x > area_size[0]:
            current_x = 0
            current_y += height

    return positions
