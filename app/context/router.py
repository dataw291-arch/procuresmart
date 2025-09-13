def route_message(user_input: str) -> str:
    """Route to Procurement or Supplier agent based on keywords."""
    if "supplier" in user_input.lower():
        return "supplier"
    return "procurement"
