
from src.models.store import Store
from src.models.product import Product
from src.models.user import User
from src.models.cart import Cart
from src.models.item import Item
from dataclasses import dataclass


@dataclass
class App:
    store: Store
    current_user: User | None

    def login(self):
        print("\n=== Iniciar sesión ===")
        for idx, _ in enumerate(self.store.users):
            number = idx + 1
            print(f"{number}. Usuario {number}")
        try:
            choice = int(input("Seleccione usuario: "))
            if 1 <= choice <= len(self.store.users):
                self.current_user = self.store.users[choice-1]
                print(f"Sesión iniciada como Usuario {choice}\n")
            else:
                print("Opción inválida.")
                self.login()
        except ValueError:
            print("Entrada inválida.")
            self.login()

    def display(self):
        print("\n=== Menú Principal ===")
        print("1. Ver productos")
        print("2. Comprar producto")
        print("3. Ver carrito")
        print("4. Eliminar producto del carrito")
        print("5. Checkout (finalizar compra)")
        print("6. Salir")

    def show_products(self):
        print("\n--- Productos Disponibles ---")
        for idx, p in enumerate(self.store.products):
            print(
                f"{idx+1}. {p.name} | {p.description} | Stock: {p.units_available} | Precio: ${p.unit_price}")

    def buy_product(self):
        self.show_products()
        try:
            idx = int(input("Seleccione producto (número): ")) - 1
            if 0 <= idx < len(self.store.products):
                product = self.store.products[idx]
                qty = int(input(f"Cantidad de '{product.name}' a comprar: "))
                if qty <= 0:
                    print("Cantidad inválida.")
                    return
                if product.units_available >= qty:
                    item = Item(product=product, qty=qty)
                    self.store.add_product_to_cart(self.current_user, item)
                    product.reduce_units(qty)
                    print(f"Agregado {qty} x {product.name} al carrito.")
                else:
                    print("No hay suficiente stock disponible.")
            else:
                print("Producto inválido.")
        except ValueError:
            print("Entrada inválida.")

    def view_cart(self):
        print("\n--- Carrito ---")
        cart = self.current_user.cart
        if not cart.items:
            print("Carrito vacío.")
            return
        for idx, item in enumerate(self.current_user.cart.items):
            print(
                f"{idx+1}. {item.product.name} x {item.qty} | Precio unitario: ${item.product.unit_price}")

    def remove_from_cart(self):
        if not self.current_user.cart.items:
            print("Carrito vacío.")
            return
        self.view_cart()
        try:
            idx = int(input("Seleccione producto a eliminar (número): ")) - 1
            if 0 <= idx < len(self.current_user.cart.items):
                item = self.current_user.cart.items[idx]
                self.store.delete_item_from_cart(self.current_user, item)
                print(f"Eliminado {item.product.name} del carrito.")
            else:
                print("Índice inválido.")
        except ValueError:
            print("Entrada inválida.")

    def checkout(self):
        cart = self.current_user.cart
        if not cart.items:
            print("Carrito vacío.")
            return
        total = 0.0
        print("\n--- Resumen de compra ---")
        for item in cart.items:
            subtotal = item.product.unit_price * item.qty
            print(f"{item.product.name} x {item.qty} = ${subtotal}")
            total += subtotal
        print(f"Total a pagar: ${total}")
        confirm = input("¿Confirmar compra? (s/n): ").lower()
        if confirm == 's':
            self.store.finish_order(self.current_user)
            print("¡Compra realizada!")
        else:
            print("Compra cancelada.")

    def start(self):
        self.login()
        while True:
            self.display()
            choice = input("Seleccione una opción: ")
            if choice == "1":
                self.show_products()
            elif choice == "2":
                self.buy_product()
            elif choice == "3":
                self.view_cart()
            elif choice == "4":
                self.remove_from_cart()
            elif choice == "5":
                self.checkout()
            elif choice == "6":
                print("Saliendo...")
                break
            else:
                print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":

    



    # Productos hardcodeados
    products = [
        Product(sku="A1", name="Manzana", description="Fruta roja",
                units_available=10, unit_price=1.5),
        Product(sku="B2", name="Pan", description="Pan integral",
                units_available=20, unit_price=2.0),
        Product(sku="C3", name="Leche", description="Leche descremada",
                units_available=15, unit_price=2.5),
    ]
    # Usuarios hardcodeados
    users = [User(cart=Cart()), User(cart=Cart())]
    store = Store(users=users, products=products)
    app = App(store)
    app.start()
