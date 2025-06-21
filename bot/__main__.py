from .mailtm import MailTM
from .instagram import InstagramAccount, InstagramBot
from .utils import generate_name, generate_username, generate_password


def main() -> None:
    mail = MailTM()
    name = generate_name()
    username = generate_username()
    password = generate_password()

    account = InstagramAccount(
        email=mail.address,
        name=name,
        username=username,
        password=password,
    )

    bot = InstagramBot(headless=False)
    try:
        bot.create_account(account)
        code = mail.get_last_code()
        if code:
            print(f"Verification code: {code}")
        else:
            print("No verification code received.")
    finally:
        bot.close()


if __name__ == "__main__":
    main()
