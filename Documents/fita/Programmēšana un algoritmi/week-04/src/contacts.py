"""Kontaktu pārvaldības grāmatiņa, kas ļauj pievienot, skatīt, 
meklēt un dzēst kontaktus, saglabājot datus JSON formātā.
Programma pārbauda vai tālruņa numurs ir derīgs Latvijas formātā un nodrošina, 
ka nav dublikātu telefona numuru. Visi numuri json faila tiek augšupielādēti formātā +371 XXXXXXXX,
 neatkarīgi no tā vai lietotājs ievada numuru ar +371 vai bez tā. Numuru salīdzināšanai tiek izmantoti
 pēdējie 8 cipari.
import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    """Nolasa kontaktus no JSON faila. Ja fails neeksistē, atgriež []."""
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_contacts(contacts):
    """Saglabā kontaktu sarakstu JSON failā."""
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

def normalize_phone(phone):
    """Atgriež tikai pēdējos 8 ciparus no tālruņa numura."""
    phone = phone.replace(" ", "")
    if phone.startswith("+371") and len(phone) == 12 and phone[4:].isdigit():
        return phone[4:]
    elif len(phone) == 8 and phone.isdigit():
        return phone
    return None

def add_contact(kontaktu_saraksts):
    """Pievieno jaunu kontaktu un saglabā to."""
    original_name = input("Ievadi kontakta vārdu: ").strip()
    name = original_name
    count = 1

    existing_names = [c['name'] for c in kontaktu_saraksts]
    while name in existing_names:
        name = f"{original_name} ({count})"
        count += 1

    while True:
        phone = input("Ievadi kontakta tālruņa numuru: ")
        normalized = normalize_phone(phone)

        if not normalized:
            if phone.strip() == "0":
                return False
            print("Kļūda: Ievadiet derīgu Latvijas numuru (8 cipari vai +371 un 8 cipari). (0 - atpakaļ)")
            continue

        existing = next(
            (c for c in kontaktu_saraksts if normalize_phone(c['phone']) == normalized),
            None
        )
        if existing:
            print(f"Kļūda: Šis numurs jau eksistē kontaktam '{existing['name']}'.")
            continue

        formatted_phone = f"+371 {normalized}"
        break

    kontaktu_saraksts.append({"name": name, "phone": formatted_phone})
    print(f"Kontakts '{name}' ar tālruni {formatted_phone} ir pievienots.")
    return True

def view_contacts(kontaktu_saraksts):
    """Parāda visus kontaktus."""
    if not kontaktu_saraksts:
        print("Nav neviena kontakta.")
        return
    sorted_contacts = sorted(kontaktu_saraksts, key=lambda x: x['name'].lower())
    print("Kontakti:")
    for i, contact in enumerate(sorted_contacts, start=1):
        print(f"{i}. {contact['name']}: {contact['phone']}")

def search_contact(kontaktu_saraksts):
    """Meklē kontaktu pēc vārda vai tālruņa numura."""
    if not kontaktu_saraksts:
        print("Nav neviena kontakta.")
        return

    query = input("Meklēt (vārds vai numurs): ").strip().lower()
    normalized_query = normalize_phone(query)

    results = [
        c for c in kontaktu_saraksts
        if query in c['name'].lower() or
        (normalized_query and normalize_phone(c['phone']) == normalized_query)
    ]

    if results:
        sorted_results = sorted(results, key=lambda x: x['name'].lower())
        print(f"Atrasti {len(results)} kontakti:")
        for i, contact in enumerate(sorted_results, start=1):
            print(f"{i}. {contact['name']}: {contact['phone']}")
    else:
        print("Nekas nav atrasts.")

def delete_contact(kontaktu_saraksts):
    """Dzēš kontaktu pēc numura, visus ar 'all', atpakaļ ar '0'."""
    if not kontaktu_saraksts:
        print("Nav neviena kontakta.")
        return False

    view_contacts(kontaktu_saraksts)
    izvele = input("Kontakta nr. (all - dzēst visus, 0 - atpakaļ): ").strip().lower()

    if izvele == "0":
        return False

    if izvele == "all":
        kontaktu_saraksts.clear()
        print("Visi kontakti ir dzēsti.")
        return True

    try:
        nr = int(izvele)
        sorted_contacts = sorted(kontaktu_saraksts, key=lambda x: x['name'].lower())

        if nr < 1 or nr > len(sorted_contacts):
            print("Kļūda: Tāds numurs neeksistē.")
            return False

        contact = sorted_contacts[nr - 1]
        kontaktu_saraksts.remove(contact)
        print(f"Kontakts '{contact['name']}' ir dzēsts.")
        return True
    except ValueError:
        print("Kļūda: Ievadiet skaitli, 'all' vai '0'.")
        return False

if __name__ == "__main__":
    contacts = load_contacts()

    while True:
        print("\n1. Pievienot kontaktu\n2. Rādīt kontaktus\n3. Meklēt kontaktu\n4. Dzēst kontaktus\n5. Iziet")
        izvele = input("Izvēle: ").strip()

        if izvele == "1":
            add_contact(contacts)
            save_contacts(contacts)
        elif izvele == "2":
            view_contacts(contacts)
        elif izvele == "3":
            search_contact(contacts)
        elif izvele == "4":
            if delete_contact(contacts):
                save_contacts(contacts)
        elif izvele == "5":
            print("Progamma izslēgta.")
            break