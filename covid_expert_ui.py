import tkinter as tk
from tkinter import messagebox, ttk

# ---------------- SIMPLE RULE ENGINE ----------------
class SimpleCovidExpert:
    def __init__(self):
        # Two rules (required by your lab)
        self.rules = [
            {
                "name": "Rule 1: Fever + Loss of Taste/Smell",
                "conditions": ["fever", "loss_taste_smell"],
                "conclusion": {
                    "label": "Likely COVID-19",
                    "confidence": "High",
                    "advice": "Seek medical advice and isolate. Consider getting a PCR test."
                }
            },
            {
                "name": "Rule 2: Fever + Cough",
                "conditions": ["fever", "cough"],
                "conclusion": {
                    "label": "Possible COVID-19",
                    "confidence": "Medium",
                    "advice": "Self-isolate, monitor symptoms and consider testing."
                }
            }
        ]

        # Default rule
        self.default = {
            "label": "Low likelihood of COVID-19",
            "confidence": "Low",
            "advice": "Could be normal flu. Monitor your condition and seek help if symptoms worsen."
        }

    def evaluate(self, facts):
        for rule in self.rules:
            if all(cond in facts for cond in rule["conditions"]):
                return rule, rule["conclusion"]
        return None, self.default


# ---------------- GUI ----------------
class CovidExpertUI:
    def __init__(self, root):
        self.root = root
        self.root.title("COVID-19 Expert System")
        self.root.geometry("560x420")
        self.root.resizable(False, False)

        self.engine = SimpleCovidExpert()

        # Left panel
        left = ttk.Frame(root, padding=16)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left, text="Select Symptoms:", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W, pady=(0, 8))

        # Checkboxes
        self.symptoms_vars = {
            "fever": tk.BooleanVar(),
            "cough": tk.BooleanVar(),
            "sore_throat": tk.BooleanVar(),
            "shortness_breath": tk.BooleanVar(),
            "loss_taste_smell": tk.BooleanVar(),
            "recent_exposure": tk.BooleanVar()
        }

        checks = [
            ("Fever (temp > 37.5°C)", "fever"),
            ("Cough", "cough"),
            ("Sore throat", "sore_throat"),
            ("Shortness of breath", "shortness_breath"),
            ("Loss of taste or smell", "loss_taste_smell"),
            ("Recent close contact with COVID-19 case", "recent_exposure")
        ]

        for text, key in checks:
            ttk.Checkbutton(left, text=text, variable=self.symptoms_vars[key]).pack(anchor=tk.W, pady=2)

        # Buttons
        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill=tk.X, pady=(12, 0))

        ttk.Button(btn_frame, text="Diagnose", command=self.run_diagnosis).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Reset", command=self.reset).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="Show Rules", command=self.show_rules).pack(side=tk.LEFT, padx=(8, 0))

        # Right panel
        right = ttk.Frame(root, padding=16)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right, text="Result", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)
        self.result_var = tk.StringVar(value="No diagnosis yet.")
        ttk.Label(right, textvariable=self.result_var, wraplength=240).pack(anchor=tk.W, pady=(6, 10))

        ttk.Label(right, text="Confidence", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)
        self.confidence_var = tk.StringVar(value="-")
        ttk.Label(right, textvariable=self.confidence_var).pack(anchor=tk.W, pady=(6, 10))

        ttk.Label(right, text="Advice / Next steps", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)
        self.advice_text = tk.Text(right, height=7, width=34, wrap=tk.WORD)
        self.advice_text.pack(anchor=tk.W, pady=(6, 10))
        self.advice_text.config(state=tk.DISABLED)

        ttk.Label(right, text="Rule Fired", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)
        self.explain_var = tk.StringVar(value="No rule fired yet.")
        ttk.Label(right, textvariable=self.explain_var, wraplength=240).pack(anchor=tk.W)

    # ---------------- Logic ----------------
    def run_diagnosis(self):
        facts = {k for k, v in self.symptoms_vars.items() if v.get()}
        rule, conclusion = self.engine.evaluate(facts)

        self.result_var.set(conclusion["label"])
        self.confidence_var.set(conclusion["confidence"])

        self.advice_text.config(state=tk.NORMAL)
        self.advice_text.delete("1.0", tk.END)
        self.advice_text.insert(tk.END, conclusion["advice"])
        self.advice_text.config(state=tk.DISABLED)

        if rule:
            self.explain_var.set(f"Fired: {rule['name']}")
        else:
            self.explain_var.set("Default rule applied.")

        if "recent_exposure" in facts and conclusion["confidence"] in ("High", "Medium"):
            messagebox.showinfo("Important", "You have recent exposure. Please isolate and get tested.")

    def reset(self):
        for v in self.symptoms_vars.values():
            v.set(False)

        self.result_var.set("No diagnosis yet.")
        self.confidence_var.set("-")
        self.explain_var.set("No rule fired yet.")

        self.advice_text.config(state=tk.NORMAL)
        self.advice_text.delete("1.0", tk.END)
        self.advice_text.config(state=tk.DISABLED)

    def show_rules(self):
        win = tk.Toplevel(self.root)
        win.title("Rules")
        win.geometry("420x200")

        ttk.Label(win, text="Expert System Rules", font=("Segoe UI", 12, "bold")).pack(pady=8)

        txt = tk.Text(win, wrap=tk.WORD)
        txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        for r in self.engine.rules:
            txt.insert(tk.END, f"{r['name']}:\n")
            txt.insert(tk.END, "  IF " + " AND ".join(r["conditions"]) + "\n")
            txt.insert(tk.END, f"  THEN {r['conclusion']['label']} ({r['conclusion']['confidence']})\n\n")

        txt.insert(tk.END, f"Default rule: {self.engine.default['label']} ({self.engine.default['confidence']})")
        txt.config(state=tk.DISABLED)


# ---------------- MAIN ----------------
def main():
    root = tk.Tk()
    app = CovidExpertUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
