from dataclasses import dataclass
from src.models.store import Store
from src.models.product import Product
from src.models.user import User
from src.models.cart import Cart
from src.models.item import Item
from src.models.rules_manager import RulesManager
from src.models.product_rule import RegularProductRule, WeightBasedProductRule, SpecialProductRule
from src.models.console import Console
from src.models.options import Options
from src.models.option import Option
from src.utils.list_manipulation import ListManipulation


@dataclass
class App:
    store: Store
    ui: Console
    current_user: User | None = None
    options: Options | None = None
    users: list[User]

    def login(self):
        self.ui.show_message("\n=== Iniciar sesión ===")
        for idx, user in enumerate(self.users):
            self.ui.show_message(
                f"{idx+1}. Usuario {idx+1} {'(Admin)' if user.is_admin else ''}")

        user = ListManipulation.select_from_list(self.users, "Seleccione usuario: ", self.ui)
        if user:
            self.current_user = user
            self.ui.show_message(f"Sesión iniciada\n")
            self.set_options()
        else:
            self.login()

    def display_menu(self):
        self.ui.show_message("\n=== Menú Principal ===")
        self.options.show_options(self.current_user)

    def view_total_sales(self):
        self.ui.show_message("\n=== Ventas Totales ===")
        total_sales = self.store.total_sales
        self.ui.show_message(f"Total de ventas: ${total_sales}")

    def show_products(self):
        self.ui.show_message("\n--- Productos Disponibles ---")
        for idx, p in enumerate(self.store.products):
            self.ui.show_message(
                f"{idx+1}. {p.name} | {p.description} | Stock: {p.units_available} | Precio: ${p.unit_price}"
            )

    def buy_product(self):
        self.show_products()
        product: Product = ListManipulation.select_from_list(
            self.store.products, "Seleccione producto (número): ", self.ui)
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
        item: Item = ListManipulation.select_from_list(
            cart.items, "Seleccione producto a eliminar (número): ", self.ui)
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

    def set_options(self):

        ALL_OPTIONS = [
            Option(text="Ver total de ventas",
                   action=app.view_total_sales, admin_only=True),
            Option(text="Ver productos", action=app.view_products),
            Option(text="Ver carrito", action=app.view_cart),
            Option(text="Seleccionar producto", action=app.buy_product),
            Option(text="Eliminar del carrito", action=app.remove_from_cart),
            Option(text="Finalizar compra", action=app.checkout),
            Option(text="Cambiar perfil", action=app.login),
            Option(text="Salir", action=app.exit_app),
        ]

        is_admin = self.current_user.is_admin

        options = []

        if is_admin:
            options = [opt for opt in ALL_OPTIONS if opt.admin_only]
        else:
            options = [opt for opt in ALL_OPTIONS if not opt.admin_only]

        self.options = Options(options=options)

    def start(self):
        self.login()
        while True:
            self.display_menu()
            selected_option = ListManipulation.select_from_list(self.options.options, "Seleccione una opción: ", self.ui)
            if selected_option:
                selected_option.action()


if __name__ == "__main__":
    products = [
        Product(sku="WE", name="Manzana", description="Fruta roja",
                units_available=10, unit_price=1.5),
        Product(sku="SP", name="Pan", description="Pan integral",
                units_available=20, unit_price=2.0),
        Product(sku="EA", name="Leche", description="Leche descremada",
                units_available=15, unit_price=2.5),
    ]

    RulesManager.add_rule(RegularProductRule)
    RulesManager.add_rule(WeightBasedProductRule)
    RulesManager.add_rule(SpecialProductRule)

    users = [User(), User(), User(is_admin=True)]

    store = Store(products=products)

    ui = Console()
    app = App(store=store, ui=ui, users=users)

    app.start()
