import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from requests.exceptions import RequestException, ConnectionError, Timeout
from colorama import Fore, Style, init
import time  


init(autoreset=True)


def ensure_protocol(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url


def should_ignore(url):
    ignore_keywords = ['cpcontacts', 'mail','webdisk', 'www','sso','ojs','ojs1','ojs2','cloud','dev', 'cpcalendars', 'cpanel', 'api', 'cpcontacts', 'ns1', 'mail']
    return any(keyword in url for keyword in ignore_keywords)


def check_phpmyadmin(url, found_file):
    if should_ignore(url):
        print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Ignoring URL (contains restricted keyword): {url}")
        return

    try:
        url_with_protocol = ensure_protocol(url)
        full_url = url_with_protocol.rstrip('/') + '/phpmyadmin'
        
        print(f"\n{Fore.CYAN}[INFO]{Style.RESET_ALL} Check: {full_url}")
        response = requests.get(full_url, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else 'No Title Found'

            if 'phpmyadmin' in title.lower():
                print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL} found phpMyAdmin: {full_url}")
                found_file.write(full_url + '\n')

            print(f"    {Fore.WHITE}[STATUS]{Style.RESET_ALL} Title: {title}")
            print(f"    {Fore.WHITE}[STATUS]{Style.RESET_ALL} HTTP Status: {response.status_code}")
        else:
            print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Not found phpmyadmin: {full_url}")
            print(f"    {Fore.WHITE}[STATUS]{Style.RESET_ALL} HTTP Status: {response.status_code}")

    except ConnectionError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Connection failed for {url}: tidak bisa menjangkau domain")
    except Timeout:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Timeout occurred for {url}: Request timed out.")
    except RequestException as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error with {url}: {e}")


def check_websites(websites):
    with open("found-pma.txt", "a") as found_file:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for website in websites:
                executor.submit(check_phpmyadmin, website, found_file)


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


print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Starting scanning process...")
time.sleep(3)  


file_path = 'list.txt'
websites = load_websites_from_file(file_path)


if websites:
    check_websites(websites)
else:
    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} No websites to process.")
