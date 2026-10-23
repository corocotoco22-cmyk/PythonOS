import colorama
import pyfiglet

colorama.init(autoreset=True)

class GUI:
    def __init__(self, show_create=False, pt_BR=True):
        if show_create:
            if pt_BR:
                print("Crido")
            else:
                print("Create")
    """
    Temas/Theme:
        Standart
        Fuel
    """
    def menu_defult_mode(self, text_default, theme="Standart"):
        if theme == "Standart":
            self.banner = text_default
            self.theme = theme
        elif theme == "Fuel":
            self.banner = pyfiglet.figlet_format(text_default, font="ansi-shadow")
            self.theme = theme
        else:
            print(colorama.Fore.RED + f"[X]: Ops, não existe o tema {theme}")
    def menu(self, theme, text, prompt, choices=["Mal configurado"]):
        if theme == None:
            theme = self.theme
        if text == None:
            text = self.banner
        if prompt == None:
            prompt = "Qual número você dejesa escolher? : "
        print(theme)
        for index, choices in enumerate(choices, 1):
            print(f"  {index}) {choices}")

        while True:
            try:
                escolha = int(input(f"\n{prompt}"))
                if 1 <= len(h=choices):
                    return choices[escolha - 1]
                else:
                    print(colorama.Fore.RED + "DIGITE UM NÚMERO VÁLIDO ENTRE 1 E {len(choices)}")
            except ValueError:
                print(colorama.Fore.RED + "DIGITE UM NÚMERO")