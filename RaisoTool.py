#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ForestSpeed v5.1 - Ultimate Group DM Tool (Auto Rename + Auto Send)
# Fixed & Tested on Termux - November 2025

import os
import time
import random
import requests
import threading
import itertools
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

# Colors (نستخدم Fore فقط عشان ما يطلع خطأ في تيرموكس)
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
M = Fore.MAGENTA
C = Fore.CYAN
W = Fore.WHITE
LR = Fore.LIGHTRED_EX
LG = Fore.LIGHTGREEN_EX
LY = Fore.LIGHTYELLOW_EX
LC = Fore.LIGHTCYAN_EX
LM = Fore.LIGHTMAGENTA_EX
LB = Fore.LIGHTBLUE_EX
RESET = Fore.RESET

def clear():
    os.system('clear')

def banner():
    clear()
    print(f"""{R}
┌──────────────────────────────────────┐
│ ██████╗  █████╗ ██╗███████╗ ██████╗ │
│ ██╔══██╗██╔══██╗██║██╔════╝██╔═══██╗│
│ ██████╔╝███████║██║███████╗██║   ██║│
│ ██╔═══╝ ██╔══██║██║╚════██║██║   ██║│
│ ██║     ██║  ██║██║███████║╚██████╔╝│
│ ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝ ╚═════╝ │
│            R A I S O T O O L          │
└──────────────────────────────────────┘                            
          Raisotool v3 - Group DM Dominator{RESET}
         {Y}Auto Rename + Auto Send Messages Simultaneously{RESET}
                {LC}Made for Termux - 100% Working{RESET}
{RESET}""")

def loading():
    banner()
    for char in "Starting Raisotool...":
        print(f"{LC}{char}", end='', flush=True)
        time.sleep(0.05)
    print(f"\n{LG}Engine Ready! Group is about to burn...{RESET}\n")
    time.sleep(1)

def get_token():
    while True:
        token = input(f"{W} ┌─ Token ➜ {G}").strip()
        if len(token) > 50: return token
        print(f"{R}   Invalid token! Too short.{RESET}")

def get_group_id():
    while True:
        gid = input(f"{W} ┌─ Group DM ID ➜ {C}").strip()
        if gid.isdigit() and len(gid) >= 17: return gid
        print(f"{R}   Invalid Group ID!{RESET}")

def get_delay():
    while True:
        try:
            d = float(input(f"{W} ┌─ Delay (seconds) ➜ {Y}") or "1")
            if d >= 0: return d
        except: pass
        print(f"{R}   Enter a valid number!{RESET}")

def get_names():
    names = []
    print(f"\n{LM}Enter names for Auto Rename (type 'done' to finish):")
    while True:
        name = input(f"   {W}➤ {RESET}").strip()
        if name.lower() == "done":
            if len(names) < 0:
                print(f"{R}   Need at least 0 names!{RESET}")
                continue
            break
        if name:
            names.append(name[:100])
            print(f"   {G}Added → {name[:40]}{'...' if len(name)>40 else ''}{RESET}")
    return names

def get_messages():
    messages = []
    print(f"\n{LB}Enter messages to spam (type 'done' to finish):")
    while True:
        msg = input(f"   {W}➤ {RESET}").strip()
        if msg.lower() == "done":
            if not messages:
                print(f"{R}   Need at least 1 message!{RESET}")
                continue
            break
        if msg:
            messages.append(msg)
            print(f"   {LG}Added → {msg[:40]}{'...' if len(msg)>40 else ''}{RESET}")
    return messages

def rename_loop(token, group_id, names, delay):
    url = f"https://discord.com/api/v10/channels/{group_id}"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    for name in itertools.cycle(names):
        if not threading.main_thread().is_alive(): break
        try:
            requests.patch(url, headers=headers, json={"name": name[:100]}, timeout=8)
        except: pass
        time.sleep(delay + random.uniform(0.3, 0.9))

def spam_loop(token, group_id, messages, delay):
    url = f"https://discord.com/api/v10/channels/{group_id}/messages"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    count = 0
    for msg in itertools.cycle(messages):
        if not threading.main_thread().is_alive(): break
        count += 1
        try:
            r = requests.post(url, headers=headers, json={"content": msg}, timeout=8)
            status = f"{LG}SENT" if r.status_code == 200 else f"{R}FAILED"
            print(f"{W}[{count:04d}] {status} ➤ {LY}{msg[:50]}{RESET}")
        except:
            print(f"{R}[{count:04d}] NETWORK ERROR{RESET}")
        time.sleep(delay + random.uniform(0.4, 1))

def main():
    loading()
    token = get_token()
    group_id = get_group_id()
    delay = get_delay()
    names = get_names()
    messages = get_messages()

    # Test access
    test = requests.get(f"https://discord.com/api/v10/channels/{group_id}",
                       headers={"Authorization": token})
    if test.status_code != 200:
        print(f"\n{R}Cannot access Group DM! Check ID or token.{RESET}")
        exit()
    current = test.json().get("name", "Unknown")
    print(f"\n{LG}Target: {LY}{current}{RESET}\n")

    input(f"{LR}Press ENTER to activate RaisoTool... (Ctrl+C to stop){RESET}")
    banner()
    print(f"{LR}╔══════════════════════════════════════════════════╗")
    print(f"{LR}║            Raisotool is activated!      ║")
    print(f"{LR}╚══════════════════════════════════════════════════╝{RESET}\n")

    t1 = threading.Thread(target=rename_loop, args=(token, group_id, names, delay), daemon=True)
    t2 = threading.Thread(target=spam_loop, args=(token, group_id, messages, delay), daemon=True)
    t1.start()
    t2.start()

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        clear()
        banner()
        print(f"{LR}RaisoTool Group has been destroyed successfully.{RESET}")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        os.system("pip install requests colorama")
        main()