from .utils.hash_tools import generate_hash
from .utils.base64_tools import encode_b64, decode_b64
from .utils.leakcheck import check_leak
from .utils.telegram_send import send_telegram


def menu() -> str:
    print("\nHERMES LITE - Menu Principal")
    print("1. Gerar Hash (MD5/SHA256)")
    print("2. Codificar Base64")
    print("3. Decodificar Base64")
    print("4. Verificar e-mail no LeakCheck")
    print("5. Enviar mensagem via Telegram")
    print("6. Sair")
    return input("> ")


def main() -> None:
    while True:
        choice = menu()
        if choice == "1":
            text = input("Texto: ")
            method = input("Método (md5/sha256): ").lower()
            try:
                print("Hash:", generate_hash(text, method))
            except ValueError as err:
                print(err)
        elif choice == "2":
            text = input("Texto: ")
            print("Base64:", encode_b64(text))
        elif choice == "3":
            text = input("Base64: ")
            try:
                print("Texto:", decode_b64(text))
            except ValueError as err:
                print(err)
        elif choice == "4":
            query = input("E-mail ou usuário: ")
            try:
                print("Resultado:", check_leak(query))
            except Exception as err:
                print(f"Erro: {err}")
        elif choice == "5":
            msg = input("Mensagem: ")
            try:
                send_telegram(msg)
                print("Enviado.")
            except Exception as err:
                print(f"Falha ao enviar: {err}")
        elif choice == "6":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
