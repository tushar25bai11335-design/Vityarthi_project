# Simple Grocery Budget Helper
def find_total(item_list):
    total = 0.0
    for item in item_list:
        name = item[0]
        qty = item[1]
        price = item[2]
        total = total + qty * price
    return total

def give_suggestion(item_list, total, budget):
    if budget <= 0:
        return "Next time decide a proper budget first."

    if total <= budget:
        return "Nice. You stayed inside your budget."

    snack_words = ["chips", "biscuit", "biscuits", "namkeen", "maggi",
                   "cold drink", "soft drink", "chocolate", "ice cream"]

    snack_total = 0.0
    non_ess_total = 0.0

    for item in item_list:
        name = item[0].lower()
        qty = item[1]
        price = item[2]
        cat = item[3].lower()
        cost = qty * price

        if cat == "non-essential":
            non_ess_total = non_ess_total + cost

        for word in snack_words:
            if word in name:
                snack_total = snack_total + cost
                break

    if snack_total > 0:
        return "Budget gone high. Try to cut down on snacks and junk items."
    elif non_ess_total > 0:
        return "Budget gone high mainly due to non-essential items."
    else:
        return "Budget crossed. Try to control overall grocery spending."


def show_items(item_list):
    if not item_list:
        print("No items added yet.")
        return

    print("\nItems you added:")
    print("----------------------------------------------")
    print("No.  Name              Qty  Type        Amount")
    print("----------------------------------------------")

    count = 1
    for item in item_list:
        name = item[0]
        qty = item[1]
        price = item[2]
        cat = item[3]
        cost = qty * price
        print(f"{count:<4} {name:<16} {qty:<4} {cat:<10} ₹{cost:.2f}")
        count = count + 1

    print("----------------------------------------------")


def show_category_total(item_list):
    essential_sum = 0.0
    non_essential_sum = 0.0

    for item in item_list:
        qty = item[1]
        price = item[2]
        cat = item[3].lower()
        cost = qty * price
        if cat == "essential":
            essential_sum = essential_sum + cost
        else:
            non_essential_sum = non_essential_sum + cost

    print("\nCategory wise total:")
    print("Essential items      : ₹{:.2f}".format(essential_sum))
    print("Non-essential items  : ₹{:.2f}".format(non_essential_sum))


def change_item(item_list):
    if not item_list:
        print("No items to change.")
        return

    show_items(item_list)

    try:
        idx = int(input("Enter item number to edit: "))
    except ValueError:
        print("Wrong input.")
        return

    if idx < 1 or idx > len(item_list):
        print("Item number not valid.")
        return

    item = item_list[idx - 1]
    print("\nEditing:", item[0])

    new_name = input("New name (Enter to keep same): ").strip()
    if new_name != "":
        item[0] = new_name

    new_qty = input("New quantity (Enter to keep same): ").strip()
    if new_qty != "":
        try:
            q = int(new_qty)
            if q >= 0:
                item[1] = q
        except ValueError:
            print("Invalid quantity, keeping old.")

    new_price = input("New price (Enter to keep same): ").strip()
    if new_price != "":
        try:
            p = float(new_price)
            if p >= 0:
                item[2] = p
        except ValueError:
            print("Invalid price, keeping old.")

    new_cat = input("New type (Essential/Non-essential, Enter to keep same): ").strip()
    if new_cat != "":
        item[3] = new_cat

    print("Item updated.")


def remove_item(item_list):
    if not item_list:
        print("No items to delete.")
        return

    show_items(item_list)
    try:
        idx = int(input("Enter item number to delete: "))
    except ValueError:
        print("Wrong input.")
        return

    if idx < 1 or idx > len(item_list):
        print("Item number not valid.")
        return

    removed = item_list.pop(idx - 1)
    print("Deleted item:", removed[0])


def put_discount(total):
    try:
        d = float(input("Enter discount % (0-100): "))
    except ValueError:
        print("Invalid discount. No discount used.")
        return total

    if d < 0 or d > 100:
        print("Discount out of range. No discount used.")
        return total

    disc_amt = total * d / 100.0
    new_total = total - disc_amt
    print("Discount amount      : ₹{:.2f}".format(disc_amt))
    print("Total after discount : ₹{:.2f}".format(new_total))
    return new_total


def main():
    print("====================================")
    print("        Grocery Budget Helper       ")
    print("====================================")

    budget = float(input("Enter your monthly budget (₹): "))

    items = []
    final_total = 0.0

    while True:
        print("\n------- MENU -------")
        print("1. Add item")
        print("2. View items and total")
        print("3. Edit item")
        print("4. Delete item")
        print("5. Show category summary")
        print("6. Apply discount")
        print("7. Exit and show final result")
        print("--------------------")

        choice = input("Choose option (1-7): ").strip()

        if choice == "1":
            print("\nEnter item details:")
            name = input("Item name: ").strip()
            try:
                qty = int(input("Quantity: "))
                price = float(input("Price per unit (₹): "))
            except ValueError:
                print("Wrong quantity/price. Item not added.")
                continue

            print("Type of item: 1. Essential  2. Non-essential")
            type_choice = input("Choose (1/2): ").strip()
            if type_choice == "1":
                cat = "Essential"
            elif type_choice == "2":
                cat = "Non-essential"
            else:
                print("Invalid type. Taking as Non-essential.")
                cat = "Non-essential"

            items.append([name, qty, price, cat])
            now_total = find_total(items)
            print(f"Item added. Current total: ₹{now_total:.2f}")

            if now_total > budget:
                print("Warning: You already crossed your budget!")
            elif now_total > 0.9 * budget:
                print("Note: You are close to your budget limit.")

        elif choice == "2":
            show_items(items)
            now_total = find_total(items)
            print(f"Total spent so far : ₹{now_total:.2f}")
            print(f"Remaining budget   : ₹{budget - now_total:.2f}")

        elif choice == "3":
            change_item(items)

        elif choice == "4":
            remove_item(items)

        elif choice == "5":
            show_category_total(items)

        elif choice == "6":
            now_total = find_total(items)
            print(f"Total before discount: ₹{now_total:.2f}")
            final_total = put_discount(now_total)

        elif choice == "7":
            break

        else:
            print("Invalid choice. Enter number between 1 and 7.")

    if final_total == 0.0:
        final_total = find_total(items)

    print("\n====================================")
    print("             Final Report           ")
    print("====================================")
    show_items(items)
    print(f"Planned budget  : ₹{budget:.2f}")
    print(f"Final spending  : ₹{final_total:.2f}")

    if final_total <= budget:
        print(f"Money left      : ₹{budget - final_total:.2f}")
    else:
        print(f"Extra spent     : ₹{final_total - budget:.2f}")

    msg = give_suggestion(items, final_total, budget)
    print("\nNote:", msg)
    print("\nThanks for using this program.")


if __name__ == "__main__":
    main()


