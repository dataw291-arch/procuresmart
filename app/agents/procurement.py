import pandas as pd

PROC_FILE = "data/procedure_data.csv"

def load_procedure():
    return pd.read_csv(PROC_FILE)

def handle_procurement(user_input: str, step: int):
    """Returns the current step and guidance."""
    df = load_procedure()
    if step >= len(df):
        return "✅ Procurement process completed."
    row = df.iloc[step]
    return f"Step {row['Step']}: {row['Name']}\nInstruction: {row['Instruction']}\nNext: {row['Next']}"

