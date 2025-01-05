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
    ignore_keywords = ['cpcontacts', 'mail','webdisk', 'www','sso','ojs','ojs1','ojs2','cloud','dev', 'cpcalendars', 'cpanel', 'api', 'cpcontacts', 'ns1','mail']
    return any(keyword in url for keyword in ignore_keywords)


def check_logout(url, found_logout_file):
    if should_ignore(url):
        print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Ignoring URL (contains restricted keyword): {url}")
        return

    try:
        url_with_protocol = ensure_protocol(url)
        full_url = url_with_protocol.rstrip('/') + '/logout'
        
        print(f"\n{Fore.CYAN}[INFO]{Style.RESET_ALL} Checking: {full_url}")
        
        
        response = requests.get(full_url, timeout=10, allow_redirects=True)

        
        if response.history:
            for resp in response.history:
                print(f"[INFO] Redirected from: {resp.url} with status: {resp.status_code}")

        
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title Found'
        
        
        if title and 'whoops! there was an error' in title.lower():
            print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL} Found debug: {full_url}")
            found_logout_file.write(f"{full_url}\n")  
        else:
            print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Title check failed for {full_url}. Title: {title}")

    except ConnectionError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Connection failed for {url}: Unable to reach the domain.")
    except Timeout:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Timeout occurred for {url}: Request timed out.")
    except RequestException as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error with {url}: {e}")


def check_websites(websites):
    with open("found-debug.txt", "a") as found_logout_file:
        with ThreadPoolExecutor(max_workers=20) as executor:
            for website in websites:
                executor.submit(check_logout, website, found_logout_file)


def load_websites_from_file(file_path):
    websites = []
    try:
        with open(file_path, 'r') as file:
            websites = [line.strip() for line in file.readlines() if line.strip()]
        print(f"\n{Fore.CYAN}[INFO]{Style.RESET_ALL} Loaded {len(websites)} websites from {file_path}")
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error: file {file_path} gada")
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


print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Starting Scann..")
time.sleep(3)  #


file_path = 'list.txt'
websites = load_websites_from_file(file_path)


if websites:
    check_websites(websites)
else:
    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} gada web yang dapat di proses")
