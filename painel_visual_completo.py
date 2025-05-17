from tkinter import Tk, Button
from reciclador_inteligente_scanner import scan


def main() -> None:
    root = Tk()
    root.title('Painel')
    Button(root, text='Executar Scanner', command=scan).pack(padx=20, pady=20)
    root.mainloop()


if __name__ == '__main__':
    main()
