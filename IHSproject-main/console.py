import os
import time
import random

# https://www.delftstack.com/howto/python/python-clear-console/
clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")


def typing(text: str, interval: float = 0.08):
    for i in text:
        print(i, end="", flush=True)
        time.sleep(interval)


def window_alert(text: str, x: int, y: int, max_width: int = 20):

    y_temp = y
    gotoxy(x, y_temp)

    # Resolver problema das quebras de linha
    linhas_conteudo = text.split("\n")
    for i, linha in enumerate(linhas_conteudo):
        linhas_conteudo[i] = f"{linha}{' '*(max_width-len(linha))}"
    text = "".join(linhas_conteudo)

    len_text = len(text)
    if len_text > max_width:
        print("┌{}┐".format("─" * (max_width + 2)))
    else:
        print("┌{}┐".format("─" * (len_text + 2)))

    linhas = len_text / max_width

    y_temp += 1
    gotoxy(x, y_temp)
    if linhas <= 1:
        print("│ {} │".format(text))
    else:
        c = 0
        while linhas > 0:
            if len(text[c : c + max_width]) < max_width:
                print(
                    "│ {}{} │".format(
                        text[c : c + max_width],
                        " " * (max_width - len(text[c : c + max_width])),
                    )
                )
            else:
                print("│ {} │".format(text[c : c + max_width]))
            c += max_width
            linhas -= 1
            y_temp += 1
            gotoxy(x, y_temp)

    if len_text > max_width:
        print("└{}┘".format("─" * (max_width + 2)))
    else:
        print("└{}┘".format("─" * (len_text + 2)))


def pause():
    if os.name in ("nt", "dos"):
        os.system("pause")
    else:
        input("Press the <Enter> key to continue...")


def init(lines):
    clear()
    print("\n" * lines, end="")


def reset(x, y, lines, columns):
    gotoxy(x, y)
    for i in range(lines):
        print(" " * columns)


# https://stackoverflow.com/questions/21330632/pythonic-alternative-of-gotoxy-c-code
# class COORD(ctypes.Structure):
#   _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
#
#   def __init__(self,x,y):
#       self.X = x
#       self.Y = y


def gotoxy(x, y):
    # INIT_POS = COORD(y,x)
    if os.name in ("nt", "dos"):
        print("%c[%d;%df" % (0x1B, y, x), end="", flush=True)
    #    STD_OUTPUT_HANDLE = -11
    #    hOut = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    #    ctypes.windll.kernel32.SetConsoleCursorPosition(hOut, INIT_POS)
    else:
        print("%c[%d;%df" % (0x1B, y, x), end="", flush=True)


# https://www.programcreek.com/python/example/50589/msvcrt.kbhit
# https://stackoverflow.com/questions/5044073/python-cross-platform-listening-for-keypresses

def hitKey():
    try:
        from msvcrt import getch

        return getch()
    except ImportError:
        return "\n"
