# frontend created with tkinter ( claude ai )
import tkinter as tk
from tkinter import ttk, messagebox

import calculator_backend as backend


# ---------------------------------------------------------------------------
# Shared helper for running a backend call and reporting errors nicely
# ---------------------------------------------------------------------------

def run_safely(func, *args, **kwargs):
    """Call a backend function, returning (success, result_or_error_message)."""
    try:
        return True, func(*args, **kwargs)
    except NotImplementedError as e:
        messagebox.showinfo("Not implemented yet", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))
    return False, None


# ---------------------------------------------------------------------------
# 1. Basic calculator tab
# ---------------------------------------------------------------------------

class BasicTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Enter expression:").pack(anchor="w")
        self.expr_var = tk.StringVar()
        entry = ttk.Entry(self, textvariable=self.expr_var, font=("Consolas", 14))
        entry.pack(fill="x", pady=5)
        entry.bind("<Return>", lambda e: self.compute())

        ttk.Button(self, text="Evaluate", command=self.compute).pack(anchor="w", pady=5)

        ttk.Label(self, text="Result:").pack(anchor="w", pady=(15, 0))
        self.result_var = tk.StringVar(value="—")
        ttk.Label(self, textvariable=self.result_var, font=("Consolas", 16, "bold")).pack(anchor="w")

    def compute(self):
        ok, result = run_safely(backend.evaluate_expression, self.expr_var.get())
        if ok:
            self.result_var.set(str(result))


# ---------------------------------------------------------------------------
# 2. Matrix operations tab
# ---------------------------------------------------------------------------

class MatrixTab(ttk.Frame):
    OPS = [
        "A + B", "A - B", "A x B", "Transpose A", "Inverse A",
        "Determinant A", "Eigenvalues A",
    ]

    def __init__(self, parent):
        super().__init__(parent, padding=15)

        inputs = ttk.Frame(self)
        inputs.pack(fill="x")

        col_a = ttk.Frame(inputs)
        col_a.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ttk.Label(col_a, text="Matrix A (rows on new lines, values space/comma separated)").pack(anchor="w")
        self.text_a = tk.Text(col_a, height=6, font=("Consolas", 11))
        self.text_a.pack(fill="both", expand=True)

        col_b = ttk.Frame(inputs)
        col_b.pack(side="left", fill="both", expand=True)
        ttk.Label(col_b, text="Matrix B (used for +, -, x)").pack(anchor="w")
        self.text_b = tk.Text(col_b, height=6, font=("Consolas", 11))
        self.text_b.pack(fill="both", expand=True)

        controls = ttk.Frame(self)
        controls.pack(fill="x", pady=10)
        ttk.Label(controls, text="Operation:").pack(side="left")
        self.op_var = tk.StringVar(value=self.OPS[0])
        ttk.Combobox(
            controls, textvariable=self.op_var, values=self.OPS,
            state="readonly", width=20
        ).pack(side="left", padx=10)
        ttk.Button(controls, text="Compute", command=self.compute).pack(side="left")

        ttk.Label(self, text="Result:").pack(anchor="w")
        self.output = tk.Text(self, height=8, font=("Consolas", 11), state="disabled")
        self.output.pack(fill="both", expand=True)

    def compute(self):
        try:
            a = backend.parse_matrix(self.text_a.get("1.0", "end"))
        except Exception as e:
            messagebox.showerror("Error parsing Matrix A", str(e))
            return

        op = self.op_var.get()
        needs_b = op in ("A + B", "A - B", "A x B")
        b = None
        if needs_b:
            try:
                b = backend.parse_matrix(self.text_b.get("1.0", "end"))
            except Exception as e:
                messagebox.showerror("Error parsing Matrix B", str(e))
                return

        dispatch = {
            "A + B": lambda: backend.matrix_add(a, b),
            "A - B": lambda: backend.matrix_subtract(a, b),
            "A x B": lambda: backend.matrix_multiply(a, b),
            "Transpose A": lambda: backend.matrix_transpose(a),
            "Inverse A": lambda: backend.matrix_inverse(a),
            "Determinant A": lambda: backend.matrix_determinant(a),
            "Eigenvalues A": lambda: backend.matrix_eigen(a),
        }

        ok, result = run_safely(dispatch[op])
        if ok:
            self._show(result)

    def _show(self, result):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", str(result))
        self.output.config(state="disabled")


# ---------------------------------------------------------------------------
# 3. Statistics tab
# ---------------------------------------------------------------------------

class StatsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Enter data (comma, space, or newline separated):").pack(anchor="w")
        self.text_data = tk.Text(self, height=6, font=("Consolas", 11))
        self.text_data.pack(fill="both", expand=True, pady=5)

        ttk.Button(self, text="Compute Statistics", command=self.compute).pack(anchor="w", pady=5)

        ttk.Label(self, text="Result:").pack(anchor="w", pady=(15, 0))
        self.output = tk.Text(self, height=8, font=("Consolas", 11), state="disabled")
        self.output.pack(fill="both", expand=True)

    def compute(self):
        try:
            data = backend.parse_vector(self.text_data.get("1.0", "end"))
        except Exception as e:
            messagebox.showerror("Error parsing data", str(e))
            return

        ok, summary = run_safely(backend.stats_summary, data)
        if not ok:
            return

        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        if isinstance(summary, dict):
            for key, value in summary.items():
                self.output.insert("end", f"{key:>10}: {value}\n")
        else:
            self.output.insert("1.0", str(summary))
        self.output.config(state="disabled")


# ---------------------------------------------------------------------------
# 4. Linear algebra tab
# ---------------------------------------------------------------------------

class LinAlgTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        ttk.Label(self, text="Matrix A (coefficients):").pack(anchor="w")
        self.text_a = tk.Text(self, height=6, font=("Consolas", 11))
        self.text_a.pack(fill="both", expand=True, pady=5)

        ttk.Label(self, text="Vector b (right-hand side):").pack(anchor="w")
        self.text_b = tk.Text(self, height=2, font=("Consolas", 11))
        self.text_b.pack(fill="x", pady=5)

        ttk.Button(self, text="Solve Ax = b", command=self.compute).pack(anchor="w", pady=5)

        ttk.Label(self, text="Solution x:").pack(anchor="w", pady=(15, 0))
        self.output = tk.Text(self, height=5, font=("Consolas", 11), state="disabled")
        self.output.pack(fill="both", expand=True)

    def compute(self):
        try:
            a = backend.parse_matrix(self.text_a.get("1.0", "end"))
            b = backend.parse_vector(self.text_b.get("1.0", "end"))
        except Exception as e:
            messagebox.showerror("Error parsing input", str(e))
            return

        ok, x = run_safely(backend.solve_linear_system, a, b)
        if ok:
            self.output.config(state="normal")
            self.output.delete("1.0", "end")
            self.output.insert("1.0", str(x))
            self.output.config(state="disabled")


# ---------------------------------------------------------------------------
# 5. Functions tab (trig, log, exponential, powers)
# ---------------------------------------------------------------------------

class FunctionsTab(ttk.Frame):
    FUNCS = ["sin", "cos", "tan", "exp", "log", "log10", "sqrt", "square", "cbrt"]

    def __init__(self, parent):
        super().__init__(parent, padding=15)

        row = ttk.Frame(self)
        row.pack(fill="x", pady=5)

        ttk.Label(row, text="Value:").pack(side="left")
        self.value_var = tk.StringVar()
        ttk.Entry(row, textvariable=self.value_var, width=15).pack(side="left", padx=5)

        ttk.Label(row, text="Function:").pack(side="left", padx=(15, 0))
        self.func_var = tk.StringVar(value=self.FUNCS[0])
        ttk.Combobox(
            row, textvariable=self.func_var, values=self.FUNCS,
            state="readonly", width=10
        ).pack(side="left", padx=5)

        self.degrees_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            row, text="Use degrees (trig only)", variable=self.degrees_var
        ).pack(side="left", padx=15)

        ttk.Button(self, text="Compute", command=self.compute).pack(anchor="w", pady=10)

        ttk.Label(self, text="Result:").pack(anchor="w")
        self.result_var = tk.StringVar(value="—")
        ttk.Label(self, textvariable=self.result_var, font=("Consolas", 16, "bold")).pack(anchor="w")

    def compute(self):
        try:
            value = float(self.value_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        ok, result = run_safely(
            backend.apply_function, self.func_var.get(), value, self.degrees_var.get()
        )
        if ok:
            self.result_var.set(str(result))


# ---------------------------------------------------------------------------
# Main application window
# ---------------------------------------------------------------------------

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NumPy Maths Calculator")
        self.geometry("820x620")
        self.minsize(650, 500)

        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        notebook.add(BasicTab(notebook), text="Basic")
        notebook.add(MatrixTab(notebook), text="Matrix")
        notebook.add(StatsTab(notebook), text="Statistics")
        notebook.add(LinAlgTab(notebook), text="Linear Algebra")
        notebook.add(FunctionsTab(notebook), text="Functions")


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
