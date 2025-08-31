from src.models.console import Console

class ListManipulation:

    @staticmethod
    def select_from_list(items: list, prompt: str, ui: Console):
        choice = ui.ask_int(prompt)
        if choice is None or not (1 <= choice <= len(items)):
            ui.show_message("Selección inválida.")
            return None
        return items[choice - 1]
