import os
import sys
import re
from dotenv import load_dotenv
import google.generativeai as genai
from colorama import Fore, Style

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def main():
    while True:
        print("\n" + " AI Notes ".center(25, "="))
        print(
            f"{Fore.GREEN}[1] Save Notes{Style.RESET_ALL}\n{Fore.YELLOW}[2] Free roam{Style.RESET_ALL}\n{Fore.RED}[3] Quit{Style.RESET_ALL}"
        )
        print("".center(25, "="))
        menu_choice = get_menu_choice()
        match menu_choice:
            case 1:
                save_notes()
            case 2:
                free_roam()
            case 3:
                sys.exit(f"\n{Fore.RED}PROGRAM TERMINATED{Style.RESET_ALL}\n")  # quit


def get_menu_choice():
    while True:
        try:
            menu_choice = int(input("Enter choice: "))
            if menu_choice not in {1, 2, 3}:
                print(f"\n{Fore.RED}ERROR: Please enter 1-3{Style.RESET_ALL}\n")
            else:
                return menu_choice
        except ValueError:
            print(f"\n{Fore.RED}ERROR: Choice must be an integer{Style.RESET_ALL}\n")


def save_notes():
    print("\n" + " SAVE NOTES ".center(25, "="))
    ai_prompt = get_ai_prompt()
    ai_response = get_gemini_response(ai_prompt)
    response_not_null = validate_response(ai_response)
    if response_not_null:
        print_response(ai_response)
    else:
        print(f"{Fore.RED}ERROR: No response from Gemini AI{Style.RESET_ALL}\n")
    while True:
        sc = input(
            f"Enter {Fore.GREEN}[S] to save{Style.RESET_ALL} or {Fore.YELLOW}[C] to continue{Style.RESET_ALL}: "
        ).upper()
        is_valid_sc = validate_sc(sc)
        if is_valid_sc:
            break
        else:
            print(f"\n{Fore.RED}ERROR: Please enter [S] or [C]{Style.RESET_ALL}\n")
    if sc == "S":
        file_name = get_file_name()
        write_to_file(file_name, ai_response)


def get_ai_prompt():
    while True:
        ai_prompt = input("Enter prompt: ")
        if not ai_prompt:
            print(f"\n{Fore.RED}ERROR: Prompt can not be null{Style.RESET_ALL}\n")
        else:
            return ai_prompt


def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    ai_response = [response.text]
    return ai_response


def validate_response(ai_response):
    return True if ai_response else False


def print_response(ai_response):
    for line in ai_response:
        print(f"\n{Fore.YELLOW}{line}{Style.RESET_ALL}")


def validate_sc(sc):
    return False if sc not in {"S", "C"} else True


def get_file_name():
    while True:
        file_name = input("Enter file name to save: ").strip()
        if not is_valid_filename(file_name):
            print(
                f"\n{Fore.RED}ERROR: Please enter valid file name: {Style.RESET_ALL}\n"
            )
        else:
            return file_name


def is_valid_filename(file_name):
    regex = r"^[a-zA-Z0-9_\-]+$"
    return True if re.match(regex, file_name) else False


def write_to_file(file_name, ai_response):
    folder_path = get_folder_path()
    save_path = os.path.join(folder_path, f"{file_name}.txt")
    try:
        with open(save_path, "w") as file:
            for line in ai_response:
                file.write(line)

        if os.path.exists(save_path):
            print(
                f"\n{Fore.GREEN}SUCCESS: Notes saved to{Style.RESET_ALL} {Fore.YELLOW}{save_path}{Style.RESET_ALL}"
            )

    except Exception as e:
        print(f"\n{Fore.RED}ERROR: Failed to save file{Style.RESET_ALL}\n")


def get_folder_path():
    while True:
        try:
            user_choice = int(
                input(
                    f"{Fore.GREEN}[1]{Style.RESET_ALL} Customize save path\n{Fore.YELLOW}[2]{Style.RESET_ALL} Use default save path (cwd)\nEnter choice: "
                )
            )
            if user_choice not in {1, 2}:
                print(f"\n{Fore.RED}ERROR: Please enter 1-2{Style.RESET_ALL}\n")
            else:
                break
        except ValueError:
            print(f"\n{Fore.RED}ERROR: Choice must be an integer{Style.RESET_ALL}\n")
    match user_choice:
        case 1:
            while True:
                folder_path = input("Enter desired save path: ")
                if not folder_path:
                    print(
                        f"\n{Fore.RED}ERROR: File path can not be null{Style.RESET_ALL}\n"
                    )
                else:
                    break
        case 2:
            folder_path = os.getcwd()
    return folder_path


def free_roam():
    print("\n" + " FREE-ROAM ".center(30, "="))
    while True:
        ai_prompt = get_ai_prompt()
        ai_response = get_gemini_response(ai_prompt)
        print_response(ai_response)
        while True:
            cont = input(
                f"Enter {Fore.GREEN}[C] to continue{Style.RESET_ALL} or {Fore.RED}[R] to return{Style.RESET_ALL}: "
            ).upper()
            if cont not in {"C", "R"}:
                print(f"\n{Fore.RED}ERROR: Enter [C] or [R]{Style.RESET_ALL}\n")
            else:
                break
        if cont == "C":
            continue
        else:
            return


if __name__ == "__main__":
    main()
