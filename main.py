import argparse
import json
import threading
import time

from colorama import Fore, Style, init

# SOURCES

from sources.website import scan_website
from sources.pdf_scanner import scan_pdf
from sources.wayback import scan_wayback
from sources.github import scan_github
from sources.crtsh import scan_crtsh
from sources.linkedin import scan_linkedin
from sources.commoncrawl import scan_commoncrawl
from sources.bing import scan_bing
from sources.hunter import scan_hunter
from sources.intelx import scan_intelx

from analyzer import analyze_data

# Initialize colorama
init(autoreset=True)

# Shared data
data = []

# Thread lock
lock = threading.Lock()


def banner():

    print(Fore.CYAN + Style.BRIGHT + r"""
========================================================
                ADVANCED OSINT TOOL
========================================================
        Multi-Source Email & Username Scanner
========================================================
""")


def run_source(scanner, domain):

    global data

    source_name = scanner.__name__.replace(
        "scan_", ""
    ).capitalize()

    print(Fore.YELLOW + f"[+] Scanning {source_name}...")

    try:

        result = scanner(domain)

        if result:

            with lock:
                data += result

            print(
                Fore.GREEN +
                f"[✓] {source_name} completed "
                f"({len(result)} results found)"
            )

        else:

            print(
                Fore.RED +
                f"[-] {source_name} found nothing"
            )

    except Exception as e:

        print(
            Fore.RED +
            f"[!] Error in {source_name}: {e}"
        )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain"
    )
    # INDIVIDUAL FLAGS

    parser.add_argument(
        "-w", "--website",
        action="store_true",
        help="Scan target website"
    )

    parser.add_argument(
        "-p", "--pdf",
        action="store_true",
        help="Scan PDF files"
    )

    parser.add_argument(
        "-wb", "--wayback",
        action="store_true",
        help="Scan Wayback Machine"
    )

    parser.add_argument(
        "-g", "--github",
        action="store_true",
        help="Scan GitHub"
    )

    parser.add_argument(
        "-c", "--crtsh",
        action="store_true",
        help="Scan crt.sh certificates"
    )

    parser.add_argument(
        "-ln", "--linkedin",
        action="store_true",
        help="Scan LinkedIn"
    )

    parser.add_argument(
        "-cc", "--commoncrawl",
        action="store_true",
        help="Scan CommonCrawl"
    )

    parser.add_argument(
        "-b", "--bing",
        action="store_true",
        help="Scan Bing search results"
    )

    parser.add_argument(
        "-htr", "--hunter",
        action="store_true",
        help="Scan Hunter.io"
    )

    parser.add_argument(
        "-i", "--intelx",
        action="store_true",
        help="Scan IntelX"
    )
  
    # ALL SOURCES

    parser.add_argument(
        "-all",
        action="store_true",
        help="Run all scanners"
    )

    args = parser.parse_args()

    domain = args.domain

    banner()

    print(Fore.CYAN + f"[+] Target : {domain}")

    start_time = time.time()

    selected_sources = []

    # MAP FLAGS TO FUNCTIONS

    source_map = {
        "website": scan_website,
        "pdf": scan_pdf,
        "wayback": scan_wayback,
        "github": scan_github,
        "crtsh": scan_crtsh,
        "linkedin": scan_linkedin,
        "commoncrawl": scan_commoncrawl,
        "bing": scan_bing,
        "hunter": scan_hunter,
        "intelx": scan_intelx
    }

    # RUN ALL

    if args.all:

        selected_sources = list(
            source_map.values()
        )

    else:

        for flag, scanner in source_map.items():

            if getattr(args, flag):

                selected_sources.append(scanner)

    # DEFAULT

    if not selected_sources:

        print(
            Fore.RED +
            "\n[-] No scan type selected\n"
        )

        parser.print_help()

        return

    threads = []

    # START THREADS

    for source in selected_sources:

        t = threading.Thread(
            target=run_source,
            args=(source, domain)
        )

        t.start()

        threads.append(t)

    # WAIT

    for t in threads:
        t.join()

    result = analyze_data(data)

    end_time = time.time()

    print(
        Fore.MAGENTA +
        "\n========================================================"
    )

    print(
        Fore.GREEN + Style.BRIGHT +
        "                 SCAN COMPLETED"
    )

    print(
        Fore.MAGENTA +
        "========================================================\n"
    )

    print(
        Fore.CYAN +
        f"[+] Total Emails     : "
        f"{result['total_emails']}"
    )

    print(
        Fore.CYAN +
        f"[+] Total Usernames  : "
        f"{result['total_usernames']}"
    )

    print(
        Fore.CYAN +
        f"[+] Scan Time        : "
        f"{round(end_time - start_time, 2)} sec"
    )

    print(Fore.YELLOW + "\n[+] Emails:\n")

    for email in result["emails"]:

        if isinstance(email, dict):

            print(
                Fore.WHITE +
                f" • {email.get('email')}"
            )
            

        else:

            print(
                Fore.WHITE +
                f" • {email}"
            )

    print(
        Fore.BLUE +
        "\n[+] JSON Output:\n"
    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )


if __name__ == "__main__":

    main()