import requests
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException, ConnectionError, Timeout
from colorama import Fore, Style, init
import time  


init(autoreset=True)


def ensure_protocol(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url


def should_ignore(url):
    ignore_keywords = ['cpcontacts', 'mail','webdisk', 'www','sso','ojs','ojs1','ojs2','cloud','dev', 'cpcalendars', 'cpanel', 'api', 'cpcontacts', 'ns1','mail']
    return any(keyword in url for keyword in ignore_keywords)


def check_env(url, found_env_file):
    if should_ignore(url):
        print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Mengabaikan URL (berisi kata kunci yang dibatasi): {url}")
        return

    try:
        url_with_protocol = ensure_protocol(url)
        full_url = url_with_protocol.rstrip('/') + '/.env'
        
        print(f"\n{Fore.CYAN}[INFO]{Style.RESET_ALL} Check: {full_url}")
        
        
        response = requests.get(full_url, timeout=10, allow_redirects=True)

        
        if response.status_code in [404, 403]:
            print(f"{Fore.RED}[INFO]{Style.RESET_ALL} Skipping {full_url}  status code: {response.status_code}")
            return

        
        if response.status_code == 200:
            
            if '.env' in response.text or 'application/octet-stream' in response.headers.get('Content-Type', ''):
                print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL} found env file: {full_url}")
                found_env_file.write(f"{full_url}\n")  
            else:
                print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Not found env file {full_url}.")
        else:
            print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Status code {response.status_code} for {full_url}. No action taken.")

    except ConnectionError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Connection failed for {url}: Unable to reach the domain.")
    except Timeout:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Timeout occurred for {url}: Request timed out.")
    except RequestException as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error with {url}: {e}")


def check_websites(websites):
    with open("foundenv.txt", "a") as found_env_file:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for website in websites:
                executor.submit(check_env, website, found_env_file)


def load_websites_from_file(file_path):
    websites = []
    try:
        with open(file_path, 'r') as file:
            websites = [line.strip() for line in file.readlines() if line.strip()]
        print(f"\n{Fore.CYAN}[INFO]{Style.RESET_ALL} Loaded {len(websites)} websites from {file_path}")
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error: The file {file_path} was not found.")
    return websites


def display_banner():
    print(Fore.GREEN + '''
:━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━:   
┇        Created by Mr.Spongebob                      ┇
┇        Email : kangpepes@protonmail.com             ┇
┇        visit : www.sukabumiblackhat.com             ┇                       
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    ''')
    time.sleep(2)  


display_banner()


print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Starting scann...")
time.sleep(3)  


file_path = 'list.txt'
websites = load_websites_from_file(file_path)


if websites:
    check_websites(websites)
else:
    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Gada web yang bisa di proses taro list di list.txt")
