import os
import sys
from colorama import Fore, Back, Style, init


init(autoreset=True)


def show_banner():
    print(Fore.YELLOW + "\n" + "="*50)
    print(Fore.CYAN + " " * 10 + "Mr. Spongebob wuzz here!!" + " " * 10)
    print(Fore.YELLOW + "="*50)


def run_tool1():
    os.system('python logout.py')


def run_tool2():
    os.system('python tes.py')


def run_tool3():
    os.system('python pma.py')


def main():
    
    show_banner()

    while True:
        print(Fore.GREEN + "\nPilih tool nya bre:")
        print(Fore.BLUE + "1. Cari debug laravel")
        print(Fore.BLUE + "2. Scan file env")
        print(Fore.BLUE + "3. Scan phpmyadmin")
        print(Fore.RED + "4. Keluar")

        choice = input(Fore.WHITE + "\nMasukkan pilihan (1/2/3/4): ")

        if choice == '1':
            run_tool1()
        elif choice == '2':
            run_tool2()
        elif choice == '3':
            run_tool3()
        elif choice == '':
            run_tool4()  
        elif choice == '4':
            print(Fore.RED + "Keluar dari program.")
            sys.exit(0)  
        else:
            print(Fore.YELLOW + "Pilihan tidak valid.")


if __name__ == "__main__":
    main()
