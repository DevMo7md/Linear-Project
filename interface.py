import tkinter as tk
from tkinter import ttk, messagebox
from gaussian import forward_elimination, get_solution

class GaussSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gaussian Elimination Solver")
        self.root.geometry("1000x720")
        self.root.minsize(800, 600)

        self.rows = []
        self.matrix_frame = None

        self.build_layout()

    def build_layout(self):
        # Main title
        title = ttk.Label(
            self.root,
            text="Gaussian Elimination Solver",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=(18, 4))

        subtitle = ttk.Label(
            self.root,
            text="Solve linear systems step by step",
            font=("Arial", 11)
        )
        subtitle.pack(pady=(0, 16))

        # Dimensions controls
        controls = ttk.LabelFrame(
            self.root, text="1. System dimensions", padding=12
        )
        controls.pack(fill="x", padx=20, pady=6)

        ttk.Label(controls, text="Number of equations (m):").grid(
            row=0, column=0, sticky="w", padx=(0, 8), pady=5
        )
        # Number of equations (rows)
        self.equations_var = tk.StringVar(value="3")
        ttk.Spinbox(
            controls, from_=1, to=12, width=6,
            textvariable=self.equations_var
        ).grid(row=0, column=1, sticky="w", pady=5)

        ttk.Label(controls, text="Number of variables (n):").grid(
            row=0, column=2, sticky="w", padx=(24, 8), pady=5
        )
        # Number of variables (columns)
        self.variables_var = tk.StringVar(value="3")
        ttk.Spinbox(
            controls, from_=1, to=12, width=6,
            textvariable=self.variables_var
        ).grid(row=0, column=3, sticky="w", pady=5)

        ttk.Button(
            controls, text="Create matrix", command=self.create_matrix
        ).grid(row=0, column=4, padx=(24, 0), pady=5)

        # Matrix input area
        self.matrix_section = ttk.LabelFrame(
            self.root, text="2. Enter coefficients and constants", padding=12
        )
        self.matrix_section.pack(fill="x", padx=20, pady=8)

        # Results placeholder, to connect to the algorithm later
        results = ttk.LabelFrame(
            self.root, text="3. Solution steps", padding=12
        )
        results.pack(fill="both", expand=True, padx=20, pady=(6, 12))

        self.results_text = tk.Text(
            results, height=10, wrap="word",
            font=("Courier New", 11), state="disabled"
        )
        self.results_text.pack(fill="both", expand=True)

        self.set_results(
            "Your solution steps will appear here.\n"
            "First, create the matrix and enter your values."
        )

        # Bottom actions
        actions = ttk.Frame(self.root)
        actions.pack(fill="x", padx=20, pady=(0, 16))

        ttk.Button(
            actions, text="Clear values", command=self.clear_values
        ).pack(side="left")

        ttk.Button(
            actions, text="Solve (coming next)", command=self.solve_placeholder
        ).pack(side="right")

        self.create_matrix()
    def create_matrix(self):
        try:
            m = int(self.equations_var.get()) # Rows
            n = int(self.variables_var.get()) # Columns
            if not (1 <= m <= 12 and 1 <= n <= 12):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid dimensions",
                "Enter whole numbers between 1 and 12."
            )
            return

        # Clear old matrix widgets and input references
        for widget in self.matrix_section.winfo_children():
            widget.destroy()
        self.rows = []

        ttk.Label(
            self.matrix_section,
            text="Enter each equation's coefficients, then its constant.",
            font=("Arial", 10)
        ).grid(row=0, column=0, columnspan=2 * n + 3, sticky="w", pady=(0, 8))

        header_row = 1
        for j in range(n):
            ttk.Label(
                self.matrix_section,
                text=f"x{j + 1}",
                font=("Arial", 10, "bold")
            ).grid(row=header_row, column=2 * j, padx=4, pady=4)

        ttk.Label(
            self.matrix_section, text="b",
            font=("Arial", 10, "bold")
        ).grid(row=header_row, column=2 * n + 2, padx=4, pady=4)

        for i in range(m):
            ttk.Label(self.matrix_section, text=f"Eq. {i + 1}").grid(
                row=i + 2, column=0, padx=(0, 8), pady=3, sticky="e"
            )

            row_entries = []
            for j in range(n + 1):
                entry = ttk.Entry(self.matrix_section, width=9, justify="center")
                entry.grid(
                    row=i + 2, column=2 * j + 1,
                    padx=3, pady=3, ipady=3
                )
                entry.insert(0, "0")
                row_entries.append(entry)

                if j < n - 1:
                    ttk.Label(self.matrix_section, text="+").grid(
                        row=i + 2, column=2 * j + 2, padx=1
                    )
                elif j == n - 1:
                    ttk.Label(self.matrix_section, text="=").grid(
                        row=i + 2, column=2 * n, padx=6
                    )

            self.rows.append(row_entries)

        self.set_results(
            f"Matrix created: {m} equation(s), {n} variable(s).\n"
            "Enter the coefficients and constants above."
        )

    
    def get_matrix(self):
        matrix = []
        try:
            for row_entries in self.rows:
                values = []
                for entry in row_entries:
                    raw = entry.get().strip()
                    if not raw:
                        raise ValueError("Every matrix cell must contain a number.")
                    values.append(float(raw))
                matrix.append(values)
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return None
        return matrix

    def clear_values(self):
        for row in self.rows:
            for entry in row:
                entry.delete(0, tk.END)
                entry.insert(0, "0")
        self.set_results("Values cleared. Enter your matrix to continue.")

    def solve_placeholder(self):
        matrix = self.get_matrix()
        if matrix is None:
            return

        try:
            echelon_matrix, steps, pivot_columns = (
                forward_elimination(matrix)
            )

            self.display_steps(steps)

            result_type, solution = get_solution(
                echelon_matrix, pivot_columns
            )

            self.display_solution(result_type, solution)

        except Exception as error:
            messagebox.showerror("Solver error", str(error))

    def set_results(self, text):
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", text)
        self.results_text.configure(state="disabled")

    def display_steps(self, steps):
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", tk.END)

        for index, step in enumerate(steps):
            # Display the operation first.
            self.results_text.insert(
                tk.END,
                f"Step {index}: {step['operation']}\n",
                "heading"
            )

            self.results_text.insert(
                tk.END,
                f"{step['description']}\n\n"
            )

            # Then display the matrix recorded for this step.
            matrix = step["matrix"]
            n = len(matrix[0]) - 1

            for row in matrix:
                left = "  ".join(
                    f"{value:9.4g}" for value in row[:n]
                )
                constant = f"{row[n]:9.4g}"

                self.results_text.insert(
                    tk.END,
                    f"[ {left}  | {constant} ]\n"
                )

            self.results_text.insert(tk.END, "\n" + "-" * 48 + "\n\n")

        self.results_text.tag_configure(
            "heading", font=("Arial", 11, "bold")
        )

        self.results_text.configure(state="disabled")

    def display_solution(self, result_type, solution):
        self.results_text.configure(state="normal")

        self.results_text.insert(tk.END, "\nFINAL RESULT\n")
        self.results_text.insert(tk.END, "=" * 30 + "\n")

        if result_type == "no_solution":
            self.results_text.insert(
                tk.END, "The system has NO solution.\n"
            )

        elif result_type == "infinite_solutions":
            self.results_text.insert(
                tk.END, "The system has INFINITELY MANY solutions.\n"
            )

        else:
            for i, value in enumerate(solution):
                self.results_text.insert(
                    tk.END, f"x{i + 1} = {value:.6g}\n"
                )

        self.results_text.configure(state="disabled")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = GaussSolverGUI(root)
    root.mainloop()
