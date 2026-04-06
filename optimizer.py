import pulp
import json
import pandas as pd
import os

def load_config(file_path):
    """Loads configuration from a JSON file."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def optimize_shifts(config):
    """
    Core optimization engine using PuLP.
    Solves the shift scheduling problem based on provided constraints.
    """
    # Extract data from config
    employees = config['employees']
    days = config['days']
    shifts = config['shifts']
    constraints = config['constraints']

    # 1. Define the Problem (Minimization)
    prob = pulp.LpProblem("Shift_Optimization_System", pulp.LpMinimize)

    # 2. Decision Variables
    # x[e][d][s] is 1 if employee 'e' is assigned to day 'd' and shift 's', else 0
    x = pulp.LpVariable.dicts("assign", (employees, days, shifts), cat=pulp.LpBinary)

    # 3. Objective Function: Minimize total assignments (or balance workload)
    prob += pulp.lpSum(x[e][d][s] for e in employees for d in days for s in shifts)

    # 4. Constraints
    
    # Constraint A: Minimum staff requirement for each shift
    for d in days:
        for s in shifts:
            prob += pulp.lpSum(x[e][d][s] for e in employees) >= constraints['min_staff_per_shift']

    # Constraint B: No double shifts on the same day
    if constraints.get('prevent_double_shifts', True):
        for e in employees:
            for d in days:
                prob += pulp.lpSum(x[e][d][s] for s in shifts) <= 1

    # Constraint C: Maximum weekly shifts per employee
    for e in employees:
        prob += pulp.lpSum(x[e][d][s] for d in days for s in shifts) <= constraints['max_weekly_shifts']

    # 5. Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    return prob, x

def export_to_excel(prob, x, config, filename="shift_results.xlsx"):
    """Converts optimization results into a formatted Excel table."""
    if pulp.LpStatus[prob.status] != 'Optimal':
        print("Optimization was not successful. Excel file not created.")
        return

    # Prepare data structure for Excel: Rows = Days, Columns = Shifts
    report_data = []
    for d in config['days']:
        row = {"Day": d}
        for s in config['shifts']:
            # Find employees assigned to this specific day and shift
            assigned_staff = [e for e in config['employees'] if x[e][d][s].varValue == 1]
            row[s] = ", ".join(assigned_staff)
        report_data.append(row)

    # Create DataFrame and export
    df = pd.DataFrame(report_data)
    df.to_excel(filename, index=False)
    print(f"✅ Success: Results saved to '{filename}'.")

# --- Main Execution Flow ---
if __name__ == "__main__":
    # 1. Load config
    config_data = load_config('config.json')
    
    if config_data:
        # 2. Run optimization
        # optimize_shifts fonksiyonu prob (model) ve x (variables) döner
        problem, variables = optimize_shifts(config_data)
        
        # 3. Check status using the .status attribute of the problem object
        # ÇÖZÜM BURADA: status_code = problem.status
        status_text = pulp.LpStatus[problem.status]
        
        print(f"Optimization Status: {status_text}")
        
        if status_text == 'Optimal':
            # Fonksiyona status kodunu değil, direkt problem objesini gönderiyoruz
            export_to_excel(problem, variables, config_data)
        else:
            print(f"❌ Error: Could not find an optimal solution. Status: {status_text}")
            print("Try reducing 'min_staff_per_shift' or increasing 'max_weekly_shifts' in config.json")