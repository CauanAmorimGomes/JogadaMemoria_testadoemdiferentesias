import pygame
import random
import time
import sys

# Inicializa o pygame
pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
GRID_SIZE = 4  # 4x4 grid (16 cartas, 8 pares)
MARGIN = 20
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BACKGROUND_COLOR = (50, 50, 150)
CARD_BACK_COLOR = (200, 50, 50)

# Tempo inicial para virar as cartas (em segundos)
INITIAL_FLIP_TIME = 3.0
FLIP_DECREASE = 0.05  # Redução de tempo a CADA PONTO (0.05s)

# Configura a janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Memória - Velocidade Progressiva")
clock = pygame.time.Clock()

# Fonte
font = pygame.font.SysFont('Arial', 36)

class Card:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.face_up = False
        self.matched = False
    
    def draw(self):
        if self.matched:
            pygame.draw.rect(screen, GREEN, self.rect, 0, 10)
            text = font.render(str(self.value), True, BLACK)
            screen.blit(text, (self.x + CARD_WIDTH//2 - text.get_width()//2, 
                              self.y + CARD_HEIGHT//2 - text.get_height()//2))
        elif self.face_up:
            pygame.draw.rect(screen, WHITE, self.rect, 0, 10)
            text = font.render(str(self.value), True, BLACK)
            screen.blit(text, (self.x + CARD_WIDTH//2 - text.get_width()//2, 
                              self.y + CARD_HEIGHT//2 - text.get_height()//2))
        else:
            pygame.draw.rect(screen, CARD_BACK_COLOR, self.rect, 0, 10)
            pygame.draw.rect(screen, BLACK, self.rect, 2, 10)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) and not self.matched

def create_board():
    # Cria pares de valores para as cartas
    values = list(range(1, (GRID_SIZE * GRID_SIZE) // 2 + 1)) * 2
    random.shuffle(values)
    
    # Calcula o posicionamento do grid centralizado
    grid_width = GRID_SIZE * CARD_WIDTH + (GRID_SIZE - 1) * MARGIN
    grid_height = GRID_SIZE * CARD_HEIGHT + (GRID_SIZE - 1) * MARGIN
    start_x = (WIDTH - grid_width) // 2
    start_y = (HEIGHT - grid_height) // 2 + 50
    
    # Cria as cartas
    cards = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            x = start_x + j * (CARD_WIDTH + MARGIN)
            y = start_y + i * (CARD_HEIGHT + MARGIN)
            value = values[i * GRID_SIZE + j]
            cards.append(Card(value, x, y))
    
    return cards

def show_all_cards(cards, duration):
    # Mostra todas as cartas por um tempo
    for card in cards:
        card.face_up = True
    
    # Desenha a tela
    screen.fill(BACKGROUND_COLOR)
    for card in cards:
        card.draw()
    pygame.display.flip()
    
    # Espera o tempo especificado
    time.sleep(duration)
    
    # Esconde as cartas novamente
    for card in cards:
        if not card.matched:
            card.face_up = False

def main():
    cards = create_board()
    score = 0
    flip_time = INITIAL_FLIP_TIME
    
    # Mostra todas as cartas no início
    show_all_cards(cards, flip_time)
    
    selected_cards = []
    waiting = False
    wait_time = 0
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        
        screen.fill(BACKGROUND_COLOR)
        
        # Desenha o placar
        score_text = font.render(f"Pontuação: {score}", True, WHITE)
        time_text = font.render(f"Velocidade: {max(0.5, flip_time):.1f}s", True, WHITE)
        screen.blit(score_text, (20, 20))
        screen.blit(time_text, (20, 60))
        
        # Desenha as cartas
        for card in cards:
            card.draw()
        
        # Verifica se o jogo acabou
        if all(card.matched for card in cards):
            win_text = font.render("Você ganhou! Clique para jogar novamente.", True, WHITE)
            screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - win_text.get_height()//2))
            pygame.display.flip()
            
            # Espera por um clique para reiniciar
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        waiting_for_restart = False
                        main()  # Reinicia o jogo
                clock.tick(FPS)
        
        pygame.display.flip()
        
        # Lógica de espera entre seleções
        if waiting and current_time >= wait_time:
            # Verifica se as cartas selecionadas formam um par
            if len(selected_cards) == 2:
                if selected_cards[0].value == selected_cards[1].value:
                    # Par encontrado
                    for card in selected_cards:
                        card.matched = True
                    score += 1
                    
                    # A CADA PONTO, aumenta a dificuldade (diminui o tempo)
                    flip_time = max(0.5, flip_time - FLIP_DECREASE)  # Não deixa menor que 0.5s
                
                # Vira as cartas de volta
                for card in selected_cards:
                    if not card.matched:
                        card.face_up = False
                
                selected_cards = []
            waiting = False
        
        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not waiting:
                pos = pygame.mouse.get_pos()
                for card in cards:
                    if card.is_clicked(pos) and not card.face_up and len(selected_cards) < 2:
                        card.face_up = True
                        selected_cards.append(card)
                        
                        if len(selected_cards) == 2:
                            waiting = True
                            wait_time = current_time + 1000  # Espera 1 segundo
        
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()