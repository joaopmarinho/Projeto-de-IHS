from fcntl import ioctl
import save
from console import *
from time import sleep
from random import randrange
from jogoConst import *
from jogoMath import solve2
from termios import *
import keyboard

import sys
import termios
import atexit
from select import select
from kbhit import *


def ranking(configuracoes, x: int = 1, y: int = 1) -> dict:
    opcoes = list(configuracoes["dificuldades"].keys())
    ranking = [
        "┌────────────────────────────┐",
        "│          Ranking           │",
        "├────────────────────────────┤",
    ]
    for dificuldade in opcoes:
        record = save.load_info_on_save(dificuldade)
        record = record if record != "" else "Não definido"
        ranking += [
            "│ {}: {}{}│".format(
                dificuldade, record, " " * (25 - len(dificuldade) - len(record))
            )
        ]
    ranking += [
        "└────────────────────────────┘",
    ]
    temp_y = y
    for i in ranking:
        gotoxy(x, temp_y)
        print(i)
        temp_y += 1

    gotoxy(x, temp_y)
    input("Pressione enter para voltar")


def configurar(configuracoes, x: int = 1, y: int = 1) -> dict:
    """
    Função para configurar o jogo
    """
    while True:
        clear()
        opcoes = list(configuracoes["dificuldades"].keys())

        configuracoes_menu = [
            "┌────────────────────────────┐",
            "│       Configurações        │",
            "├────────────────────────────┤",
        ]
        for i, dificuldade in enumerate(opcoes):
            configuracoes_menu += [
                "│ {} - {}{}│".format(i + 1, dificuldade, " " * (23 - len(dificuldade)))
            ]
        configuracoes_menu += [
            "├────────────────────────────┤",
            "│ ?:                         │",
            "└────────────────────────────┘",
        ]

        temp_y = y
        for i in configuracoes_menu:
            gotoxy(x, temp_y)
            print(i)
            temp_y += 1
        gotoxy(x + 5, y + 8)

        dificuldade_num = -1
        while dificuldade_num <= 0 or dificuldade_num > len(opcoes):
            try:
                dificuldade_num = int(input())
            except:
                dificuldade_num = -1
        dificuldade_num -= 1

        dificuldade_escolhida = configuracoes["dificuldades"][opcoes[dificuldade_num]]

        window_alert(
            f"    Configuração escolhida:\n  Alvos:         {dificuldade_escolhida['alvos']}\n  Velocidade:    {dificuldade_escolhida['velocidade']}\n  Limite Perder: {dificuldade_escolhida['limite_perder']}\n  Medalha: {dificuldade_escolhida['medalha']}",
            x + 31,
            y + 2,
            30,
        )

        return dificuldade_escolhida


"""
Muda com a dificuldade:
"""


def jogar(dificuldade_escolhida):
    clear()
    RD_SWITCHES   = 24929
    RD_PBUTTONS   = 24930
    WR_L_DISPLAY  = 24931
    WR_R_DISPLAY  = 24932
    WR_RED_LEDS   = 24933
    WR_GREEN_LEDS = 24934
    fd = os.open(sys.argv[1], os.O_RDWR)
    novato = False
    nomeJogador = 'Soldadinho de Jesus'
    #if nomeJogador == "":
    #    novato = True
    #    while True:
    #        nomeJogador = str(input("Digite o nome do jogador: ")).strip()
    #        if nomeJogador != "":
    #            save.save_info_on_save("nome", nomeJogador)
    #            break
    clear()

    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)


    if novato:
        typing("\nHouve um ataque alienígena na sua cidade!!\n")
        sleep(1)
        typing(
            f"\nVocê, {nomeJogador}, cidadão brasileiro descendente de Adilton de Morais, um dos veteranos da \nSegunda Guerra Mundial, vulgo Pracinhas, vai até o porão e encontra um MORTEIRO."
        )
        sleep(2)
        typing("\n\nAGORA É SUA HORA DE MOSTRAR SERVIÇO. A COBRA VAI FUMAR!!")
        sleep(2)

    init(LIMITE_VERT)

    gotoxy(0, LIMITE_VERT + 1)
    print("*" * LIMITE, end="", flush=True)
    gotoxy(0, LIMITE_VERT - 4)
    print("-" * LIMITE, end="", flush=True)
    gotoxy((LIMITE / 2) - 5, LIMITE_VERT - 3)
    print(nomeJogador, end="")
    gotoxy((LIMITE / 2) - 9, LIMITE_VERT - 2)
    print("Alvos vivos: ", end="")
    gotoxy((LIMITE / 2) - 11, LIMITE_VERT - 1)
    print("Dificuldade: " + dificuldade_escolhida["nome"], end="")

    gotoxy((LIMITE / 2) - 7, LIMITE_VERT)
    print("Tempo: ")

    window_alert(
        "Pressione enter para      iniciar",
        LIMITE / 2 - 12,
        (LIMITE_VERT - 4) / 2 - 2,
    )
    input()

    balas_laterais = [
        {"img": "o", "x": 0, "y": 0, "ativo": False, "traj": {"A": 0, "B": 0, "C": 0}},
        {"img": "o", "x": 0, "y": 0, "ativo": False, "traj": {"A": 0, "B": 0, "C": 0}},
        {"img": "o", "x": 0, "y": 0, "ativo": False, "traj": {"A": 0, "B": 0, "C": 0}},
        {"img": "o", "x": 0, "y": 0, "ativo": False, "traj": {"A": 0, "B": 0, "C": 0}},
        {"img": "o", "x": 0, "y": 0, "ativo": False, "traj": {"A": 0, "B": 0, "C": 0}},
        {"img": "o", "x": 0, "y": 0, "ativo": False, "traj": {"A": 0, "B": 0, "C": 0}},
        {"img": "o", "x": 0, "y": 0, "ativo": False, "traj": {"A": 0, "B": 0, "C": 0}},
    ]

    novodisco = []
    direcao = "cima"
    for _ in range(int(dificuldade_escolhida["alvos"])):
        direcao = "baixo" if direcao == "cima" else "cima"
        novodisco.append(
            {
                "img": "X",
                "x": 0,
                "y": 0,
                "ativo": False,
                "direcao": direcao,
                "traj": {"A": 0, "B": 0},
            }
        )

    y_do_canhao = LIMITE_VERT / 2
    pontuacaoJogador = 0.0
    numeroAlvos = len(novodisco)
    numeroVidasJogador = 3
    intervalo = 5  # Intervalo de (ciclos de espera para) lançamento de disco

    tempo_inicial = time.time()
    jogo_ativo = True
    entrada_teclado = KBHit()

    while jogo_ativo:

        gotoxy((LIMITE / 2) + 1, LIMITE_VERT)
        print(f"{round(time.time()-tempo_inicial, 2)}    ")

        gotoxy(0, LIMITE_VERT - 4)
        print("-" * LIMITE, end="", flush=True)

        # Limpa a tela toda
        for i in range(1, LIMITE_VERT - 5):
            gotoxy(0, i)
            print(" " * LIMITE)

        gotoxy(LIMITE / 2 + 5, LIMITE_VERT - 2)
        print(f"{len(novodisco)}   ", end="")
        gotoxy(dificuldade_escolhida["limite_perder"], 1)
        print("|")
        gotoxy(dificuldade_escolhida["limite_perder"], LIMITE_VERT - 5)
        print("|")

        acertou = 0
        for bala in balas_laterais:
            for p, disco in enumerate(novodisco):
                if (
                    bala["ativo"]
                    and disco["ativo"]
                    and (
                        bala["x"] == disco["x"]
                        or bala["x"] + 1 == disco["x"]
                        or bala["x"] - 1 == disco["x"]
                    )
                    and (bala["y"] == disco["y"])
                ):
                    acertou = True
                    disco["ativo"] = False
                    bala["ativo"] = False
                    novodisco.pop(p)
                    break
        if acertou:
            numeroAlvos -= 1

        if pontuacaoJogador < 0:
            numeroVidasJogador -= 1

        def fimDoJogo():
            return novodisco == []

        if fimDoJogo():
            save.save_record_on_save(
                dificuldade_escolhida["nome"], round(time.time() - tempo_inicial, 2)
            )
            gotoxy(LIMITE / 2 - 15, LIMITE_VERT / 2)
            window_alert(
                "Missão completa, "
                + nomeJogador
                + "!!\nVocê ganhou a medalha:\n"
                + dificuldade_escolhida["medalha"]
                + "!!!",
                LIMITE / 2 - 12,
                (LIMITE_VERT + 1 - 4) / 2 - 2,
                25,
            )

            data = 0b000000000000000000
            #data1 = 0b11111111
            # data to write
            ioctl(fd, WR_RED_LEDS)
            retval = os.write(fd, int(data).to_bytes(4, 'little'))
            # print("wrote %d bytes"%retval)
            #round(time.time()-tempo_inicial, 2)
            

            input()
            clear()
            break

        def gameOver():
            disco_invalido = False
            for disco in novodisco:
                if (
                    disco["x"] < dificuldade_escolhida["limite_perder"]
                    and disco["ativo"]
                ):
                    disco_invalido = True
            return disco_invalido

        if gameOver():
            gotoxy(LIMITE / 2 - 15, LIMITE_VERT / 2)
            window_alert(
                "Você falhou, " + nomeJogador + "!\nSeu BISONHO!!!!",
                LIMITE / 2 - 12,
                (LIMITE_VERT + 1 - 4) / 2 - 2,
                25,
            )
            data1 = 0b00000000

            ioctl(fd, WR_GREEN_LEDS)
            retval = os.write(fd, int(data1).to_bytes(4, 'little'))

            input()
            clear()
            break

        intervalo = len(novodisco) + randrange(10)
        j = 0
        for disco in novodisco:
            if not disco["ativo"]:
                disco["ativo"] = True
                disco["x"] = LIMITE - 2 - randrange(10)
                disco["y"] = 0 if randrange(2) % 2 == 0 else LIMITE_VERT - 5
                disco["traj"]["A"] = 0
                disco["traj"]["B"] = dificuldade_escolhida["velocidade"]
                break

        for disco in novodisco:
            if disco["ativo"]:
                gotoxy(disco["x"], disco["y"])
                print("  ", end="")
                if (
                    disco["direcao"] == "baixo"
                    and disco["y"] + disco["traj"]["B"] > LIMITE_VERT - 5
                ):
                    disco["direcao"] = "cima"
                    disco["x"] -= 2
                elif disco["direcao"] == "cima" and disco["y"] - disco["traj"]["B"] < 0:
                    disco["direcao"] = "baixo"
                    disco["x"] -= 2

                if disco["direcao"] == "baixo":
                    disco["y"] += disco["traj"]["B"]
                elif disco["direcao"] == "cima":
                    disco["y"] -= disco["traj"]["B"]
                gotoxy(disco["x"], disco["y"])
                print(disco["img"], end="")



        if True:
            #7 b d e
            ioctl(fd, RD_PBUTTONS)
            red = os.read(fd, 4); # read 4 bytes and store in red var
            red = int.from_bytes(red, 'little')
            if red == 7:
                for bala in balas_laterais:
                    if not bala["ativo"]:
                        bala["ativo"] = True
                        bala["x"] = 0
                        bala["y"] = y_do_canhao
                        bala["traj"]["C"] = bala["y"]
                        bala["traj"]["A"] = (max(-15, 4 - bala["traj"]["C"])) / (
                            (LIMITE / 2) * (LIMITE / 2 - LIMITE)
                        )
                        bala["traj"]["B"] = -bala["traj"]["A"] * LIMITE
                        break
            elif red == 11:
                gotoxy(0, y_do_canhao)
                print("  ", end="", flush=True)
                if y_do_canhao - 1 <= 4:
                    y_do_canhao = 5
                    gotoxy(5, LIMITE_VERT - 2)
                    print("Limite atingido, abaixe mais")
                else:
                    y_do_canhao -= 1
                    gotoxy(5, LIMITE_VERT - 2)
                    print(" " * 30)
            elif red == 13:
                gotoxy(0, y_do_canhao)
                print("  ", end="", flush=True)
                if y_do_canhao + 1 >= LIMITE_VERT - 4:
                    y_do_canhao = LIMITE_VERT - 5
                    gotoxy(5, LIMITE_VERT - 2)
                    print("Limite atingido, suba mais")
                else:
                    y_do_canhao += 1
                    gotoxy(5, LIMITE_VERT - 2)
                    print(" " * 30)
            elif red ==14:
                jogo_ativo = False

        j = 0
        for bala in balas_laterais:
            gotoxy(bala["x"], bala["y"])
            print("  ", end="")
            if bala["ativo"]:
                bala["x"] += 3
                bala["y"] = int(
                    solve2(
                        bala["traj"]["A"],
                        bala["traj"]["B"],
                        bala["traj"]["C"],
                        bala["x"],
                    )
                )

                if bala["x"] > LIMITE:
                    bala["ativo"] = False
                else:
                    gotoxy(bala["x"], bala["y"])
                    print(bala["img"], end="")
            j += 1

        gotoxy(0, y_do_canhao)
        print("//", end="", flush=True)

        print(end="", flush=True)
        sleep(0.05)
        intervalo -= 1