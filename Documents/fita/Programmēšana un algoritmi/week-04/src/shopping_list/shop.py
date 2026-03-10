import sys
from storage import load_list, save_list, get_price, set_price
from utils import calc_line_total, calc_grand_total, count_units


def cmd_add(args):
    if len(args) < 2:
        print("Kļūda: norādi nosaukumu un daudzumu. Piemērs: python shop.py add Maize 3")
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

    # Ja cena norādīta tieši komandrindā
    if len(args) >= 3:
        try:
            price = float(args[2])
            if price <= 0:
                print("Kļūda: cenai jābūt pozitīvam skaitlim.")
                return
        except ValueError:
            print("Kļūda: cena nav derīgs skaitlis.")
            return
        set_price(name, price)
    else:
        known_price = get_price(name)
        if known_price is not None:
            print(f"Atrasta cena: {known_price:.2f} EUR/gab.")
            choice = input("[A]kceptēt / [M]ainīt? > ").strip().lower()
            if choice == "m":
                price = _ask_price()
                if price is None:
                    return
                set_price(name, price)
                print(f"✓ Cena atjaunināta: {name} → {price:.2f} EUR")
            else:
                price = known_price
        else:
            print("Cena nav zināma.")
            price = _ask_price()
            if price is None:
                return
            set_price(name, price)
            print(f"✓ Cena saglabāta: {name} ({price:.2f} EUR)")

    item = {"name": name, "qty": qty, "price": price}
    items = load_list()
    items.append(item)
    save_list(items)
    print(f"✓ Pievienots: {name} × {qty} ({price:.2f} EUR/gab.) = {calc_line_total(item):.2f} EUR")


def _ask_price():
    """Prasa lietotājam ievadīt derīgu cenu."""
    try:
        price = float(input("Ievadi cenu: "))
        if price <= 0:
            print("Kļūda: cenai jābūt pozitīvam skaitlim.")
            return None
        return price
    except ValueError:
        print("Kļūda: cena nav derīgs skaitlis.")
        return None


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

def cmd_export():
    """Eksportē sarakstu teksta failā SMS/WhatsApp formātā."""
    items = load_list()
    if not items:
        print("Saraksts ir tukšs.")
        return

    lines = ["Iepirkumu saraksts:\n"]
    for item in items:
        lines.append(f"• {item['name']} × {item['qty']} — {calc_line_total(item):.2f} EUR")

    lines.append("")
    lines.append(f"Kopā: {calc_grand_total(items):.2f} EUR ({count_units(items)} vienības)")

    filename = "shopping_export.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ Eksportēts: {filename}")

def main():
    if len(sys.argv) < 2:
        print("Lietošana:")
        print("  python shop.py add <nosaukums> <daudzums> [cena]")
        print("  python shop.py list")
        print("  python shop.py total")
        print("  python shop.py clear")
        print("  python shop.py export")
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
    elif command == "export":
        cmd_export()
    else:
        print(f"Kļūda: nezināma komanda '{command}'.")


if __name__ == "__main__":
    main()