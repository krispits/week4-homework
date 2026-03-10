import sys
from storage import load_list, save_list
from utils import calc_line_total, calc_grand_total, count_units


def cmd_add(args):
    if len(args) < 3:
        print("Kļūda: norādi nosaukumu, daudzumu un cenu. Piemērs: python shop.py add Maize 3 1.20")
        return
    name = args[0]
    try:
        qty = int(args[1])
        if qty <= 0:
            print("Kļūda: daudzumam jābūt pozitīvam skaitlim.")
            return
    except ValueError:
        print("Kļūda: daudzums nav derīgs skaitlis.")
        return
    try:
        price = float(args[2])
        if price <= 0:
            print("Kļūda: cenai jābūt pozitīvam skaitlim.")
            return
    except ValueError:
        print("Kļūda: cena nav derīgs skaitlis.")
        return

    item = {"name": name, "qty": qty, "price": price}
    items = load_list()
    items.append(item)
    save_list(items)
    print(f"✓ Pievienots: {name} × {qty} ({price:.2f} EUR/gab.) = {calc_line_total(item):.2f} EUR")


def cmd_list():
    items = load_list()
    if not items:
        print("Saraksts ir tukšs.")
        return
    print("Iepirkumu saraksts:")
    for i, item in enumerate(items, start=1):
        print(f"  {i}. {item['name']} × {item['qty']} — {item['price']:.2f} EUR/gab. — {calc_line_total(item):.2f} EUR")


def cmd_total():
    items = load_list()
    if not items:
        print("Saraksts ir tukšs.")
        return
    print(f"Kopā: {calc_grand_total(items):.2f} EUR ({count_units(items)} vienības, {len(items)} produkti)")


def cmd_clear():
    save_list([])
    print("✓ Saraksts notīrīts.")


def main():
    if len(sys.argv) < 2:
        print("Lietošana:")
        print("  python shop.py add <nosaukums> <daudzums> <cena>")
        print("  python shop.py list")
        print("  python shop.py total")
        print("  python shop.py clear")
        return

    command = sys.argv[1].lower()

    if command == "add":
        cmd_add(sys.argv[2:])
    elif command == "list":
        cmd_list()
    elif command == "total":
        cmd_total()
    elif command == "clear":
        cmd_clear()
    else:
        print(f"Kļūda: nezināma komanda '{command}'.")


if __name__ == "__main__":
    main()