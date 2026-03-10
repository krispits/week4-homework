def calc_line_total(item):
    """Atgriež qty × price."""
    return item["qty"] * item["price"]



def calc_grand_total(items):
    total = 0
    for item in items:
        total += calc_line_total(item)
    return total


def count_units(items):
    units = 0
    for item in items:
        units += item["qty"]
    return units