def load_info_on_save(config: str) -> str:
    with open("save", "r", encoding="utf-8") as save:
        for l in list(save.readlines()):
            if config.upper() in l:
                return (l.split("="))[1].replace("\n", "")
    return ""


def save_info_on_save(config: str, value: str) -> None:
    with open("save", "r", encoding="utf-8") as save:
        linhas = []
        achou = False
        for l in list(save.readlines()):
            if config.upper() in l:
                linhas.append(f"{config.upper()}={value}\n")
                achou = True
            else:
                linhas.append(l)
        if not achou:
            linhas.append(f"{config.upper()}={value}\n")
    with open("save", "w", encoding="utf-8") as new_save:
        new_save.writelines(linhas)


def save_record_on_save(difficulty: str, record: float) -> None:
    with open("save", "r", encoding="utf-8") as save:
        linhas = []
        achou = False
        novo_record = False
        for l in list(save.readlines()):
            if difficulty.upper() in l:
                achou = True
                novo_record = float(l.split("=")[1]) > record
                if novo_record:
                    linhas.append(f"{difficulty.upper()}={record}\n")
                else:
                    linhas.append(l)
            else:
                linhas.append(l)
        if not achou and not novo_record:
            linhas.append(f"{difficulty.upper()}={record}\n")
    with open("save", "w", encoding="utf-8") as new_save:
        new_save.writelines(linhas)
