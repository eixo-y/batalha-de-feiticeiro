import pygame
import random
import sys
import time

# --- Inicialização do Pygame ---
pygame.init()

# --- Configurações da Tela ---
# MODIFICAÇÃO 1: Aumentar a largura da tela
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Batalha de Magos")

# --- Cores ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
UI_BLUE = (50, 50, 150)
UI_BORDER = (200, 200, 255)
FIRE_ORANGE = (255, 100, 0)
ICE_BLUE = (173, 216, 230)
METEOR_BROWN = (139, 69, 19)
POTION_PINK = (255, 105, 180)

# --- Fontes ---
FONT_DEFAULT = pygame.font.Font(None, 28)
FONT_CONSOLE = pygame.font.Font(None, 22)
FONT_TITLE = pygame.font.Font(None, 50)

# --- Configurações do Jogo ---
player_hp = 100
enemy_hp = 100
max_hp = 100
player_visual_hp = 100
enemy_visual_hp = 100

player_potions = 3
turn = "player"
game_log = ["A batalha começou!"]
game_over = False
winner = None

magias = {
    "bola_fogo": {"nome": "Bola de Fogo", "dano": 30, "chance": 60, "cor": FIRE_ORANGE},
    "raio_gelo": {"nome": "Raio de Gelo", "dano": 20, "chance": 80, "cor": ICE_BLUE},
    "meteoro": {"nome": "Chuva de Meteoros", "dano": 50, "chance": 30, "cor": METEOR_BROWN},
    "pocao_cura": {"nome": "Poção de Cura", "cura": 20}
}

# --- Animações ---
animation_state = None
enemy_action_time = 0

# --- Desenho dos Elementos ---

def draw_character(x, y, color, is_player):
    pygame.draw.rect(screen, color, (x, y, 50, 80))
    pygame.draw.polygon(screen, (60, 0, 120), [(x - 10, y), (x + 60, y), (x + 25, y - 40)])
    if is_player:
        pygame.draw.line(screen, (139, 69, 19), (x + 60, y + 20), (x + 80, y + 60), 5)
        pygame.draw.circle(screen, (150, 0, 255), (x + 60, y + 20), 10)
    else:
        pygame.draw.line(screen, (139, 69, 19), (x - 10, y + 20), (x - 30, y + 60), 5)

def draw_health_bar(x, y, current_hp, max_hp, color):
    ratio = current_hp / max_hp
    if ratio < 0: ratio = 0
    
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, 204, 24))
    pygame.draw.rect(screen, (100,0,0), (x, y, 200, 20))
    pygame.draw.rect(screen, color, (x, y, 200 * ratio, 20))
    
    hp_text = FONT_DEFAULT.render(f"{max(0, int(current_hp))}/{max_hp}", True, WHITE)
    screen.blit(hp_text, (x + 70, y - 1))


def draw_ui():
    pygame.draw.rect(screen, UI_BLUE, (0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200))
    pygame.draw.line(screen, UI_BORDER, (0, SCREEN_HEIGHT - 200), (SCREEN_WIDTH, SCREEN_HEIGHT - 200), 3)

    global btn_bola_fogo, btn_raio_gelo, btn_meteoro, btn_pocao
    btn_bola_fogo = pygame.Rect(20, 420, 150, 50)
    pygame.draw.rect(screen, FIRE_ORANGE, btn_bola_fogo)
    text = FONT_DEFAULT.render("Bola de Fogo", True, BLACK)
    screen.blit(text, (btn_bola_fogo.x + 15, btn_bola_fogo.y + 15))

    btn_raio_gelo = pygame.Rect(190, 420, 150, 50)
    pygame.draw.rect(screen, ICE_BLUE, btn_raio_gelo)
    text = FONT_DEFAULT.render("Raio de Gelo", True, BLACK)
    screen.blit(text, (btn_raio_gelo.x + 20, btn_raio_gelo.y + 15))

    btn_meteoro = pygame.Rect(20, 490, 150, 50)
    pygame.draw.rect(screen, METEOR_BROWN, btn_meteoro)
    text = FONT_DEFAULT.render("Meteoro", True, WHITE)
    screen.blit(text, (btn_meteoro.x + 35, btn_meteoro.y + 15))

    btn_pocao = pygame.Rect(190, 490, 150, 50)
    pygame.draw.rect(screen, POTION_PINK, btn_pocao)
    text = FONT_DEFAULT.render("Poção de Cura", True, BLACK)
    screen.blit(text, (btn_pocao.x + 10, btn_pocao.y + 15))
    
    potion_count_text = FONT_DEFAULT.render(f"{player_potions}/3", True, BLACK)
    pygame.draw.rect(screen, WHITE, (btn_pocao.right + 5, btn_pocao.y, 50, 50))
    screen.blit(potion_count_text, (btn_pocao.right + 15, btn_pocao.y + 15))

    # MODIFICAÇÃO 2: Mover o console para o lado
    console_rect = pygame.Rect(480, 420, 400, 160)
    pygame.draw.rect(screen, WHITE, console_rect)
    pygame.draw.rect(screen, BLACK, console_rect, 2)
    
    for i, line in enumerate(game_log[-7:]):
        log_text = FONT_CONSOLE.render(line, True, BLACK)
        screen.blit(log_text, (console_rect.x + 10, console_rect.y + 10 + i * 22))

def add_log(message):
    game_log.append(message)
    if len(game_log) > 20:
        game_log.pop(0)

def handle_attack(attacker_name, target_name, magia_key):
    global animation_state
    
    magia = magias[magia_key]
    add_log(f"{attacker_name} usou {magia['nome']}...")
    
    is_hit = random.randint(1, 100) <= magia["chance"]
    damage = magia["dano"] if is_hit else 0

    if attacker_name == "Você":
        start_pos = (180, 280)
        end_pos = (600, 280)
        target_pos = (625, 300)
    else:
        start_pos = (600, 280)
        end_pos = (180, 280)
        target_pos = (125, 300)

    animation_state = {
        "type": magia_key, "progress": 0.0,
        "is_hit": is_hit, "damage": damage, "target": target_name,
        "start_pos": start_pos, "end_pos": end_pos,
        "target_pos": target_pos
    }

def draw_animation():
    global animation_state
    if not animation_state:
        return

    animation_state["progress"] += 0.05
    progress = animation_state["progress"]
    
    start_x, start_y = animation_state["start_pos"]
    end_x, end_y = animation_state["end_pos"]
    
    current_x = start_x + (end_x - start_x) * progress
    current_y = start_y + (end_y - start_y) * progress

    anim_type = animation_state["type"]
    if anim_type == "bola_fogo":
        pygame.draw.circle(screen, FIRE_ORANGE, (int(current_x), int(current_y)), 15)
        pygame.draw.circle(screen, (255, 255, 0), (int(current_x), int(current_y)), 10)
    elif anim_type == "raio_gelo":
        pygame.draw.rect(screen, ICE_BLUE, (int(current_x) - 15, int(current_y) - 5, 30, 10))
    elif anim_type == "meteoro":
        target_x, target_y = animation_state["target_pos"]
        for i in range(5):
            offset_x = random.randint(-40, 40)
            meteor_y = 50 + (target_y - 50) * progress
            pygame.draw.circle(screen, METEOR_BROWN, (target_x + offset_x, int(meteor_y) + i*5), 8)

    if progress >= 1.0:
        handle_animation_end()

def handle_animation_end():
    global player_hp, enemy_hp, turn, animation_state

    if animation_state["is_hit"]:
        add_log("Acertou!")
        if animation_state["target"] == "Inimigo":
            enemy_hp -= animation_state["damage"]
        else:
            player_hp -= animation_state["damage"]
    else:
        add_log("Errou!")

    if turn == "player":
        turn = "enemy"
        global enemy_action_time
        enemy_action_time = pygame.time.get_ticks() + 1000
    else:
        turn = "player"

    animation_state = None
    check_game_over()

def check_game_over():
    global game_over, winner
    if player_hp <= 0:
        game_over = True
        winner = "Inimigo"
    elif enemy_hp <= 0:
        game_over = True
        winner = "Você"

# --- Loop Principal do Jogo ---
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if turn == "player" and not animation_state:
                if btn_bola_fogo.collidepoint(event.pos):
                    handle_attack("Você", "Inimigo", "bola_fogo")
                elif btn_raio_gelo.collidepoint(event.pos):
                    handle_attack("Você", "Inimigo", "raio_gelo")
                elif btn_meteoro.collidepoint(event.pos):
                    handle_attack("Você", "Inimigo", "meteoro")
                elif btn_pocao.collidepoint(event.pos):
                    if player_potions > 0:
                        if player_hp < max_hp:
                            player_hp += magias["pocao_cura"]["cura"]
                            if player_hp > max_hp:
                                player_hp = max_hp
                            player_potions -= 1
                            add_log("Você usou uma poção de cura (+20 HP).")
                            turn = "enemy"
                            enemy_action_time = pygame.time.get_ticks() + 1000
                        else:
                            add_log("Sua vida já está cheia.")
                    else:
                        add_log("Você não tem mais poções.")

    if turn == "enemy" and not animation_state and not game_over and pygame.time.get_ticks() > enemy_action_time:
        escolha = random.choice(["bola_fogo", "raio_gelo", "meteoro"])
        handle_attack("Inimigo", "Você", escolha)
        
    if player_visual_hp > player_hp:
        player_visual_hp -= 0.5
    elif player_visual_hp < player_hp:
        player_visual_hp += 0.5
    if enemy_visual_hp > enemy_hp:
        enemy_visual_hp -= 0.5
    elif enemy_visual_hp < enemy_hp:
        enemy_visual_hp += 0.5

    # --- Desenho ---
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, GRASS_GREEN, (0, 350, SCREEN_WIDTH, SCREEN_HEIGHT - 350))
    
    draw_character(100, 270, GREEN, is_player=True)
    draw_character(600, 270, (150, 50, 50), is_player=False)

    draw_health_bar(20, 20, player_visual_hp, max_hp, GREEN)
    # A posição da barra de vida do inimigo se ajusta automaticamente com a largura da tela
    draw_health_bar(SCREEN_WIDTH - 225, 20, enemy_visual_hp, max_hp, RED)

    draw_ui()
    draw_animation()

    if game_over:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        resultado_texto = f"{winner} venceu!" if winner == "Você" else "Você perdeu!"
        end_text = FONT_TITLE.render(resultado_texto, True, WHITE)
        text_rect = end_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(end_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()