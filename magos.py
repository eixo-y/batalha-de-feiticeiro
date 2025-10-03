import random

def inicio():
    vida = [100, 100]       # vida[0] = jogador, vida[1] = inimigo
    pocao = [3, 3]          # poções jogador e inimigo
    turno = 0               # 0 = jogador, 1 = inimigo

    magias = {
        1: {"nome": "Bola de fogo", "dano": 30, "chance": 60},
        2: {"nome": "Raio congelante", "dano": 20, "chance": 80},
        3: {"nome": "Chuva de meteoros", "dano": 50, "chance": 30},
        4: {"nome": "Poção de cura", "cura": 20}
    }

    while vida[0] > 0 and vida[1] > 0:
        if turno == 0:
            print(f"\nSua vida: {vida[0]} | Vida do inimigo: {vida[1]}")
            print("Escolha a magia:")
            for i in range(1, 5):
                if i == 4:
                    print(f"{i} - Poção de cura (cura: +{magias[i]['cura']})")
                else:
                    print(f"{i} - {magias[i]['nome']} (dano: {magias[i]['dano']}, chance: {magias[i]['chance']}%)")
            try:
                poder = int(input("Opção: "))
            except ValueError:
                poder = 0  # entrada inválida
        else:
            poder = random.randint(1,4)

        if poder in [1, 2, 3]:
            chance = random.randint(1, 100)
            magia = magias[poder]
            if chance <= magia["chance"]:
                vida_alvo = 1 - turno  # se jogador ataca inimigo e vice-versa
                vida[vida_alvo] -= magia["dano"]
                if turno == 0:
                    print(f"Você lançou {magia['nome'].lower()}... acertou!")
                else:
                    print(f"Inimigo lançou {magia['nome'].lower()}... acertou!")
            else:
                if turno == 0:
                    print(f"Você lançou {magia['nome'].lower()}... errou.")
                else:
                    print(f"Inimigo lançou {magia['nome'].lower()}... errou.")

        elif poder == 4:
            if pocao[turno] > 0 and vida[turno] <= 80:
                vida[turno] += magias[4]["cura"]
                pocao[turno] -= 1
                if turno == 0:
                    print("Você usou uma poção e recuperou 20 de vida.")
                else:
                    print("Inimigo usou uma poção e recuperou 20 de vida.")
            elif vida[turno] > 80:
                if turno == 0:
                    print("Você já tem vida o suficiente.")
                else:
                    print("Inimigo já tem vida o suficiente.")
            else:
                if turno == 0:
                    print("Você não tem mais poções.")
                else:
                    print("Inimigo não tem mais poções.")
        else:
            if turno == 0:
                print("Sua varinha quebrou e você errou o feitiço!")
            else:
                print("Inimigo errou o feitiço!")

        turno = 1 - turno  # troca de turno

    # Resultado
    if vida[0] > 0:
        print("\nVocê ganhou!!")
    else:
        print("\nVocê perdeu :(")

inicio()