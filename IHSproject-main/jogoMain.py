import json
import console
from jogoConst import LIMITE, LIMITE_VERT
import jogo
import os, sys
from fcntl import ioctl

global dificuldade_escolhida
global configuracoes

configuracoes = json.load(open("config.json", mode="r", encoding="utf-8"))
dificuldade_escolhida = configuracoes["dificuldades"]["Treino"]
save = open("save", "a")
save.close()


def exibirMenu(x: int = 1, y: int = 1) -> None:
    # largura = 30 altura = 10
    # x = COLUNA  y = LINHA
    menu = [
        "┌────────────────────────────┐",
        "│   Morteiro dos Pracinhas   │",
        "├────────────────────────────┤",
        "│ 1 - Jogar                  │",
        "│ 2 - Configurações          │",
        "│ 3 - Rankings               │",
        "│ 4 - Como jogar             │",
        "│ 5 - Sair                   │",
        "├────────────────────────────┤",
        "│ ?:                         │",
        "└────────────────────────────┘",
    ]
    temp_y = y
    for i in menu:
        console.gotoxy(x, temp_y)
        print(i)
        temp_y += 1
    console.gotoxy(x + 5, y + 9)


def como_jogar(x: int = 1, y: int = 1):
    console.window_alert(
        "  O jogo consiste em atirar com o morteiro para\nacertar os alvos na tela, caso acerte todos, você\nganha, mas caso eles passam de um limite escolhido\ncom base na dificuldade você perder.\n\n  Use W e S para subir e descer o morteiro, espaço\npara atirar e M para voltar para o menu.\n\n                   BOA SORTE!!",
        x - 10,
        y,
        50,
    )
    console.gotoxy(x - 10, y + 11)
    input("Pressione enter para voltar")


while True:
    RD_SWITCHES   = 24929
    RD_PBUTTONS   = 24930
    WR_L_DISPLAY  = 24931
    WR_R_DISPLAY  = 24932
    WR_RED_LEDS   = 24933
    WR_GREEN_LEDS = 24934

    fd = os.open(sys.argv[1], os.O_RDWR)


    data = 0b111111111111111111
    data1 = 0b11111111
    # data to write
    ioctl(fd, WR_RED_LEDS)
    retval = os.write(fd, int(data).to_bytes(4, 'little'))
    # print("wrote %d bytes"%retval)

    ioctl(fd, WR_GREEN_LEDS)
    retval = os.write(fd, int(data1).to_bytes(4, 'little'))

    data5 = 0xffffffff;
    ioctl(fd, WR_L_DISPLAY)
    retval = os.write(fd, data5.to_bytes(4, 'little'))

    data = 0xffffffff;
    ioctl(fd, WR_R_DISPLAY)
    retval = os.write(fd, data.to_bytes(4, 'little'))

    x, y = (LIMITE / 2 - 15, (LIMITE_VERT + 1) / 2 - 5)
    red1 = 0
    console.init(LIMITE_VERT)
    while red1 not in [0x1, 0x2, 0x4, 0x8, 0x10]:
        console.clear()
        exibirMenu(x, y)
        try:
            ioctl(fd, RD_SWITCHES)
            red1 = os.read(fd, 4); # read 4 bytes and store in red var
            red1 = int.from_bytes(red1, 'little')
        except:
            red1 = 0

        if red1 == 1:
            console.clear()
            data5 = 0x40824082;
            ioctl(fd, WR_L_DISPLAY)
            retval = os.write(fd, data5.to_bytes(4, 'little'))

            data = 0xf9909999;
            ioctl(fd, WR_R_DISPLAY)
            retval = os.write(fd, data.to_bytes(4, 'little'))
            jogo.jogar(dificuldade_escolhida)
        elif red1 == 2:
            console.clear()
            dificuldade_escolhida = jogo.configurar(configuracoes, x, y)
        elif red1 == 4:
            console.clear()
            jogo.ranking(configuracoes, x, y)
        elif red1 == 8:
            console.clear()
            como_jogar(x, y)
        elif red1 == 16:
            print("Bye bye!")
            exit(0)
        else:
            continue
            