import sys
from storage import load_list, save_list


def cmd_add(args):
    if len(args) < 2:
        print("Kļūda: norādi nosaukumu un cenu. Piemērs: python shop.py add Maize 1.20")
        return
    name = args[0]
    try:
        price = float(args[1])
        if price <= 0:
            print("Kļūda: cenai jābūt pozitīvam skaitlim.")
            return
    except ValueError:
        print("Kļūda: cena nav derīgs skaitlis.")
        return

    items = load_list()
    items.append({"name": name, "price": price})
    save_list(items)
    print(f"✓ Pievienots: {name} ({price:.2f} EUR)")


def cmd_list():
    items = load_list()
    if not items:
        print("Saraksts ir tukšs.")
        return
    print("Iepirkumu saraksts:")
    for i, item in enumerate(items, start=1):
        print(f"  {i}. {item['name']} — {item['price']:.2f} EUR")


def cmd_total():
    items = load_list()
    if not items:
        print("Saraksts ir tukšs.")
        return
    total = 0
    for item in items:
        total += item["price"]
    print(f"Kopā: {total:.2f} EUR ({len(items)} produkti)")


def cmd_clear():
    save_list([])
    print("✓ Saraksts notīrīts.")


def main():
    if len(sys.argv) < 2:
        print("Lietošana:")
        print("  python shop.py add <nosaukums> <cena>")
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