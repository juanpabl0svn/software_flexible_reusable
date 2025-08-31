from dataclasses import dataclass
from src.models.store import Store
from src.models.product import Product
from src.models.user import User
from src.models.cart import Cart
from src.models.item import Item
from src.models.rules_manager import RulesManager
from src.models.price_rule import RegularPriceRule, WeightBasedPriceRule, SpecialPriceRule
from src.models.console import Console
from src.models.options import Options
from src.models.option import Option


@dataclass
class App:
    store: Store
    ui: Console
    current_user: User | None = None
    options: Options | None = None

    def set_options(self, options: Options):
        self.options = options

    def select_from_list(self, items: list, prompt: str):
        choice = self.ui.ask_int(prompt)
        if choice is None or not (1 <= choice <= len(items)):
            self.ui.show_message("Selección inválida.")
            return None
        return items[choice - 1]

    def login(self):
        self.ui.show_message("\n=== Iniciar sesión ===")
        for idx, _ in enumerate(self.store.users):
            self.ui.show_message(f"{idx+1}. Usuario {idx+1}")

        user = self.select_from_list(self.store.users, "Seleccione usuario: ")
        if user:
            self.current_user = user
            self.ui.show_message(f"Sesión iniciada como {user}\n")
        else:
            self.login()

    def display_menu(self):
        self.ui.show_message("\n=== Menú Principal ===")
        self.options.show_options()

    def show_products(self):
        self.ui.show_message("\n--- Productos Disponibles ---")
        for idx, p in enumerate(self.store.products):
            self.ui.show_message(
                f"{idx+1}. {p.name} | {p.description} | Stock: {p.units_available} | Precio: ${p.unit_price}"
            )

    def buy_product(self):
        self.show_products()
        product: Product = self.select_from_list(
            self.store.products, "Seleccione producto (número): ")
        if not product or not product.has_units():
            self.ui.show_message("Producto inválido o sin stock.")
            return

        qty = self.ui.ask_float(f"Cantidad de '{product.name}' a comprar: ")
        if not qty or qty <= 0:
            self.ui.show_message("Cantidad inválida.")
            return

        if product.units_available < qty:
            self.ui.show_message("No hay suficiente stock disponible.")
            return

        qty = product.get_qty(qty)

        self.store.add_product_to_cart(self.current_user, product, qty)

        self.ui.show_message(f"Agregado {qty} x {product.name} al carrito.")

    def view_cart(self):
        self.ui.show_message("\n--- Carrito ---")
        cart = self.current_user.cart
        if not cart.items:
            self.ui.show_message("Carrito vacío.")
            return
        for idx, item in enumerate(cart.items):
            self.ui.show_message(
                f"{idx+1}. {item.product.name} x {item.qty} | Precio unitario: ${item.product.unit_price}"
            )

    def remove_from_cart(self):
        cart = self.current_user.cart
        if not cart.items:
            self.ui.show_message("Carrito vacío.")
            return

        self.view_cart()
        item: Item = self.select_from_list(
            cart.items, "Seleccione producto a eliminar (número): ")
        if not item:
            return

        self.store.delete_item_from_cart(self.current_user, item)
        self.ui.show_message(f"Eliminado {item.product.name} del carrito.")

    def checkout(self):
        cart = self.current_user.cart
        if not cart.items:
            self.ui.show_message("Carrito vacío.")
            return

        if not self.store.can_purchase(self.current_user):
            self.ui.show_message(
                "No hay suficiente stock para completar la compra.")
            return

        self.ui.show_message("\n--- Resumen de compra ---")
        cart.show_items_prices()
        total = cart.calculate_total()
        self.ui.show_message(f"Total a pagar: ${total}")

        confirm = self.ui.ask_input("¿Confirmar compra? (s/n): ").lower()
        if confirm == "s":
            self.store.finish_order(self.current_user)
            self.ui.show_message("¡Compra realizada!")
        else:
            self.ui.show_message("Compra cancelada.")

    def view_products(self):
        self.ui.show_message("\n--- Productos Disponibles ---")
        for idx, p in enumerate(self.store.products):
            self.ui.show_message(
                f"{idx+1}. {p.name} | {p.description} | Stock: {p.units_available} | Precio: ${p.unit_price}"
            )

    def exit_app(self):
        self.ui.show_message("Saliendo...")
        raise SystemExit

    def start(self):
        if not self.options:
            raise ValueError("Options are required.")

        self.login()
        while True:
            self.display_menu()
            choice = self.ui.ask_int("Seleccione una opción: ")
            if choice is None:
                continue
            self.options.execute_option(choice)


if __name__ == "__main__":
    products = [
        Product(sku="WE", name="Manzana", description="Fruta roja",
                units_available=10, unit_price=1.5),
        Product(sku="SP", name="Pan", description="Pan integral",
                units_available=20, unit_price=2.0),
        Product(sku="EA", name="Leche", description="Leche descremada",
                units_available=15, unit_price=2.5),
    ]

    RulesManager.add_rule(RegularPriceRule)
    RulesManager.add_rule(WeightBasedPriceRule)
    RulesManager.add_rule(SpecialPriceRule)

    users = [User(), User(), User()]

    store = Store(users=users, products=products)

    ui = Console()
    app = App(store=store, ui=ui)

    options_list = [
        Option(text="Ver productos", action=app.view_products),
        Option(text="Ver carrito", action=app.view_cart),
        Option(text="Seleccionar producto", action=app.buy_product),
        Option(text="Eliminar del carrito", action=app.remove_from_cart),
        Option(text="Finalizar compra", action=app.checkout),
        Option(text="Cambiar perfil", action=app.login),
        Option(text="Salir", action=app.exit_app),
    ]

    options = Options(options=options_list)

    app.set_options(options)

    app.start()
