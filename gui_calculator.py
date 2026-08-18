"""
gui_calculator.py

A tkinter maths calculator with separate tabbed sections:
    1. Basic       - arithmetic expression evaluator
    2. Matrix      - add / subtract / multiply / transpose / inverse / det / eigen
    3. Statistics  - mean / median / std / var / min / max / sum on a dataset
    4. Linear Algebra - solve Ax = b
    5. Functions   - sin / cos / tan / exp / log / sqrt / square / cbrt

This file only handles the GUI. All maths is delegated to calculator_backend.py,
which you can implement using numpy — this file already calls every backend
function and displays whatever comes back, so you don't need to touch the GUI
code to add your maths logic.

Run with:
    python gui_calculator.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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

        ttk.Label(self, text="Enter expression: (see functions for trig expressions)").pack(anchor="w")
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
# 6. Graphing tab
# ---------------------------------------------------------------------------

class GraphTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        controls = ttk.Frame(self)
        controls.pack(fill="x")

        ttk.Label(controls, text="f(x) =").pack(side="left")
        self.expr_var = tk.StringVar(value="sin(x)")
        ttk.Entry(controls, textvariable=self.expr_var, width=25, font=("Consolas", 12)).pack(
            side="left", padx=5
        )

        ttk.Label(controls, text="x min:").pack(side="left", padx=(15, 0))
        self.xmin_var = tk.StringVar(value="-10")
        ttk.Entry(controls, textvariable=self.xmin_var, width=8).pack(side="left", padx=5)

        ttk.Label(controls, text="x max:").pack(side="left")
        self.xmax_var = tk.StringVar(value="10")
        ttk.Entry(controls, textvariable=self.xmax_var, width=8).pack(side="left", padx=5)

        ttk.Label(controls, text="points:").pack(side="left")
        self.points_var = tk.StringVar(value="500")
        ttk.Entry(controls, textvariable=self.points_var, width=8).pack(side="left", padx=5)

        ttk.Button(controls, text="Plot", command=self.compute).pack(side="left", padx=15)

        # Matplotlib figure embedded inside the tkinter frame
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

        # Toolbar gives zoom / pan / save-as-image controls, same as Jupyter's
        # interactive matplotlib widgets
        toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(fill="x")

    def compute(self):
        try:
            x_min = float(self.xmin_var.get())
            x_max = float(self.xmax_var.get())
            num_points = int(self.points_var.get())
        except ValueError:
            messagebox.showerror("Error", "x min / x max / points must be numbers.")
            return

        ok, data = run_safely(
            backend.generate_plot_data, self.expr_var.get(), x_min, x_max, num_points
        )
        if not ok:
            return

        x, y = data
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.set_title(self.expr_var.get())
        self.canvas.draw()


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
        notebook.add(GraphTab(notebook), text="Graph")


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
