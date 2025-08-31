class Console:
    def show_message(self, message: str):
        print(message)

    def ask_input(self, prompt: str) -> str:
        return input(prompt)

    def ask_int(self, prompt: str) -> int | None:
        try:
            return int(input(prompt))
        except ValueError:
            self.show_message("Entrada inválida.")
            return None


    def ask_float(self, prompt: str) -> float | None:
        try:
            return float(input(prompt))
        except ValueError:
            self.show_message("Entrada inválida.")
            return None