class Category:
    def __init__(self, name: str):
        self.name = name

        self.ledger = []
        self.balance = 0.0

    def __str__(self):
        return "\n".join([f"{self.name:*^30s}",
                          *(f"{state['description']: <23s}"[:23] + f"{state['amount']: >7.2f}"[:7] for state in
                            self.ledger),
                          f"Total: {self.balance:.2f}"
                          ])

    def deposit(self, amount: float, description: str = ""):
        self.balance += amount
        self.ledger.append({"amount": amount, "description": description})
        return True

    def withdraw(self, amount: float, description: str = ""):
        if self.check_funds(amount):
            return self.deposit(-amount, description)
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount: float, another: 'Category'):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {another.name}")
            another.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False

    def check_funds(self, amount):
        return (self.balance - amount) >= 0


def create_spend_chart(categories: list):
    all_spent = [sum([-state["amount"] for state in category.ledger if state["amount"] < 0])
                 for category in categories]
    total = sum(all_spent)
    max_len = max(len(category.name) for category in categories)
    category_strings = [f"{'o' * (1 + int(spent // (total / 10))):>11s}-{category.name:<{max_len}}"
                        for spent, category in zip(all_spent, categories)]

    space = f"{' ' * 11}-{' ' * max_len}"
    labels = [f"{'1':<{12 + max_len}}",
              f"{'0987654321':<{12 + max_len}}",
              f"{'00000000000':<{12 + max_len}}",
              f"{'|||||||||||':<{12 + max_len}}"]

    columns = [*labels, *(elem for category_string in category_strings for elem in (space, category_string, space)),
               space]
    return "\n".join(
        ("Percentage spent by category",
         *["".join(row) for row in zip(*columns)])
    )

if __name__ == '__main__':
    food, entertainment, business = Category("Food"), Category("Entertain"), Category("Business")

    food.deposit(900, "deposit")
    entertainment.deposit(900, "deposit")
    business.deposit(900, "deposit")
    food.withdraw(105.55)
    entertainment.withdraw(33.40)
    business.withdraw(10.99)

    mass = create_spend_chart([food, entertainment, business])
    print(mass)
