def forward_elimination(matrix, eps=1e-10):

    A = [row[:] for row in matrix]

    m = len(A) # Number of equations (rows)
    n = len(A[0]) - 1  # Number of variables (columns)

    steps = []
    pivot_columns = []
    pivot_row = 0

    def save_step(operation, description):
        
        steps.append({
            "operation": operation,
            "description": description,
            "matrix": [row[:] for row in A]
        })

    save_step(
        "Initial augmented matrix",
        "The matrix entered by the user."
    )

    for col in range(n):

        if pivot_row >= m:
            break

        
        candidate = max(
            range(pivot_row, m),
            key=lambda r: abs(A[r][col])
        )

        if abs(A[candidate][col]) < eps:
            
            continue

        
        if candidate != pivot_row:
            A[pivot_row], A[candidate] = (
                A[candidate], A[pivot_row]
            )

            save_step(
                f"R{pivot_row + 1} <-> R{candidate + 1}",
                "Swap rows to obtain a nonzero pivot."
            )

        pivot = A[pivot_row][col]
        pivot_columns.append(col)

        
        for target_row in range(pivot_row + 1, m):
            value = A[target_row][col]

            if abs(value) < eps:
                A[target_row][col] = 0.0
                continue

            factor = value / pivot

            
            for j in range(n + 1):
                A[target_row][j] -= (
                    factor * A[pivot_row][j]
                )

                
                if abs(A[target_row][j]) < eps:
                    A[target_row][j] = 0.0

            
            if factor >= 0:
                operation = (
                    f"R{target_row + 1} = "
                    f"R{target_row + 1} - "
                    f"{factor:.4g}*R{pivot_row + 1}"
                )
            else:
                operation = (
                    f"R{target_row + 1} = "
                    f"R{target_row + 1} + "
                    f"{abs(factor):.4g}*R{pivot_row + 1}"
                )

            save_step(
                operation,
                f"Eliminate the entry in column {col + 1}."
            )

        pivot_row += 1

    return A, steps, pivot_columns

def get_solution(echelon_matrix, pivot_columns, eps=1e-10):
    rows = len(echelon_matrix)
    cols = len(echelon_matrix[0]) - 1

    
    for row in echelon_matrix:
        if all(abs(value) < eps for value in row[:cols]):
            if abs(row[cols]) >= eps:
                return "no_solution", None

    
    if len(pivot_columns) < cols:
        return "infinite_solutions", None

    
    solution = [0.0] * cols

    for i in range(len(pivot_columns) - 1, -1, -1):
        pivot_col = pivot_columns[i]
        rhs = echelon_matrix[i][cols]

        for j in range(pivot_col + 1, cols):
            rhs -= echelon_matrix[i][j] * solution[j]

        pivot = echelon_matrix[i][pivot_col]
        solution[pivot_col] = rhs / pivot

    return "unique_solution", solution