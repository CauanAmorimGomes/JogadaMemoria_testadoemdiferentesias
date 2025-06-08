import tkinter as tk
import random
import time

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Memória")
        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.score = 0
        self.delay = 1000  # tempo de exibição em ms

        self.create_board()

    def create_board(self):
        self.cards = list(range(1, 9)) * 2  # 8 pares
        random.shuffle(self.cards)
        self.revealed = [False] * 16

        for i in range(16):
            btn = tk.Button(self.root, text=" ", width=8, height=4,
                            command=lambda i=i: self.reveal_card(i))
            btn.grid(row=i // 4, column=i % 4)
            self.buttons.append(btn)

        self.status = tk.Label(self.root, text="Pontos: 0")
        self.status.grid(row=4, column=0, columnspan=4)

    def reveal_card(self, index):
        if self.revealed[index] or self.second_card is not None:
            return

        self.buttons[index].config(text=str(self.cards[index]))
        self.buttons[index].update()

        if self.first_card is None:
            self.first_card = index
        else:
            self.second_card = index
            self.root.after(self.delay, self.check_match)

    def check_match(self):
        first = self.first_card
        second = self.second_card

        if self.cards[first] == self.cards[second]:
            self.revealed[first] = True
            self.revealed[second] = True
            self.score += 1
            self.status.config(text=f"Pontos: {self.score}")

            # Aumenta dificuldade a cada 10 pontos
            if self.score % 10 == 0 and self.delay > 200:
                self.delay -= 100
                print(f"[DIFICULDADE] Novo delay: {self.delay}ms")

        else:
            self.buttons[first].config(text=" ")
            self.buttons[second].config(text=" ")

        self.first_card = None
        self.second_card = None

        if all(self.revealed):
            self.status.config(text=f"Fim de jogo! Pontuação final: {self.score}")

# Executar o jogo
if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
