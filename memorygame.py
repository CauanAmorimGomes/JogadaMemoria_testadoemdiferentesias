import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

class JogoDaMemoriaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧠 Jogo da Memória - Velocidade Progressiva")
        self.root.geometry("600x700")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Variáveis do jogo
        self.cores = ['red', 'blue', 'green', 'yellow']
        self.nomes_cores = ['VERMELHO', 'AZUL', 'VERDE', 'AMARELO']
        self.sequencia = []
        self.entrada_jogador = []
        self.pontuacao = 0
        self.velocidade_base = 1.2
        self.jogando = False
        self.mostrando_sequencia = False
        self.posicao_atual = 0
        
        self.criar_interface()
        
    def calcular_velocidade(self):
        """Calcula a velocidade atual baseada na pontuação"""
        reducao = (self.pontuacao // 10) * 0.15
        velocidade_atual = max(0.3, self.velocidade_base - reducao)
        return velocidade_atual
    
    def criar_interface(self):
        """Cria toda a interface gráfica"""
        # Título
        titulo_frame = tk.Frame(self.root, bg='#2c3e50')
        titulo_frame.pack(pady=20)
        
        titulo = tk.Label(titulo_frame, text="🧠 JOGO DA MEMÓRIA", 
                         font=('Arial', 24, 'bold'), 
                         fg='#ecf0f1', bg='#2c3e50')
        titulo.pack()
        
        subtitulo = tk.Label(titulo_frame, text="Velocidade aumenta a cada 10 pontos!", 
                           font=('Arial', 12), 
                           fg='#bdc3c7', bg='#2c3e50')
        subtitulo.pack()
        
        # Frame de informações
        info_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        info_frame.pack(pady=20, padx=20, fill='x')
        
        # Pontuação
        self.label_pontuacao = tk.Label(info_frame, text="PONTUAÇÃO: 0", 
                                       font=('Arial', 16, 'bold'), 
                                       fg='#e74c3c', bg='#34495e')
        self.label_pontuacao.pack(side='left', padx=20, pady=10)
        
        # Velocidade
        self.label_velocidade = tk.Label(info_frame, text=f"VELOCIDADE: {self.velocidade_base:.1f}s", 
                                        font=('Arial', 16, 'bold'), 
                                        fg='#f39c12', bg='#34495e')
        self.label_velocidade.pack(side='right', padx=20, pady=10)
        
        # Frame dos botões coloridos (4x4 grid para ficar mais visual)
        self.botoes_frame = tk.Frame(self.root, bg='#2c3e50')
        self.botoes_frame.pack(pady=30)
        
        self.botoes = []
        cores_layout = [
            ['red', 'blue'],
            ['green', 'yellow']
        ]
        
        nomes_layout = [
            ['VERMELHO', 'AZUL'],
            ['VERDE', 'AMARELO']
        ]
        
        for i, linha_cores in enumerate(cores_layout):
            for j, cor in enumerate(linha_cores):
                btn = tk.Button(self.botoes_frame, 
                              text=nomes_layout[i][j],
                              font=('Arial', 16, 'bold'),
                              width=12, height=4,
                              bg=cor,
                              fg='white' if cor in ['red', 'blue', 'green'] else 'black',
                              relief='raised',
                              bd=4,
                              state='disabled',
                              activebackground=cor,
                              command=lambda c=cor: self.botao_clicado(c))
                btn.grid(row=i, column=j, padx=10, pady=10)
                self.botoes.append(btn)
        
        # Frame de status
        self.status_frame = tk.Frame(self.root, bg='#2c3e50')
        self.status_frame.pack(pady=20)
        
        self.label_status = tk.Label(self.status_frame, 
                                   text="Clique em 'NOVO JOGO' para começar!", 
                                   font=('Arial', 14), 
                                   fg='#95a5a6', bg='#2c3e50')
        self.label_status.pack()
        
        # Frame de controles
        controles_frame = tk.Frame(self.root, bg='#2c3e50')
        controles_frame.pack(pady=20)
        
        self.btn_novo_jogo = tk.Button(controles_frame, 
                                      text="🎮 NOVO JOGO", 
                                      font=('Arial', 14, 'bold'),
                                      bg='#27ae60', fg='white',
                                      width=15, height=2,
                                      relief='raised', bd=3,
                                      command=self.novo_jogo)
        self.btn_novo_jogo.pack(side='left', padx=10)
        
        self.btn_parar = tk.Button(controles_frame, 
                                  text="⏹️ PARAR", 
                                  font=('Arial', 14, 'bold'),
                                  bg='#e74c3c', fg='white',
                                  width=15, height=2,
                                  relief='raised', bd=3,
                                  state='disabled',
                                  command=self.parar_jogo)
        self.btn_parar.pack(side='right', padx=10)
        
        # Instruções
        instrucoes_frame = tk.Frame(self.root, bg='#34495e', relief='sunken', bd=2)
        instrucoes_frame.pack(pady=20, padx=20, fill='x')
        
        instrucoes = tk.Label(instrucoes_frame, 
                            text="📋 INSTRUÇÕES:\n"
                                 "• Memorize a sequência de cores que pisca\n"
                                 "• Clique nas cores na mesma ordem\n"
                                 "• A cada 10 pontos a velocidade aumenta!\n"
                                 "• Tente fazer a maior pontuação possível!",
                            font=('Arial', 10),
                            fg='#ecf0f1', bg='#34495e',
                            justify='left')
        instrucoes.pack(pady=10)
    
    def novo_jogo(self):
        """Inicia um novo jogo"""
        self.sequencia = []
        self.entrada_jogador = []
        self.pontuacao = 0
        self.posicao_atual = 0
        self.jogando = True
        
        self.atualizar_interface()
        self.btn_novo_jogo.config(state='disabled')
        self.btn_parar.config(state='normal')
        
        self.label_status.config(text="Preparando nova rodada...", fg='#f39c12')
        self.root.after(1000, self.proxima_rodada)
    
    def parar_jogo(self):
        """Para o jogo atual"""
        self.jogando = False
        self.mostrando_sequencia = False
        
        for btn in self.botoes:
            btn.config(state='disabled')
        
        self.btn_novo_jogo.config(state='normal')
        self.btn_parar.config(state='disabled')
        
        self.label_status.config(text=f"Jogo parado! Pontuação final: {self.pontuacao}", 
                               fg='#e74c3c')
    
    def proxima_rodada(self):
        """Inicia a próxima rodada"""
        if not self.jogando:
            return
            
        # Adiciona nova cor à sequência
        nova_cor = random.choice(self.cores)
        self.sequencia.append(nova_cor)
        
        self.entrada_jogador = []
        self.posicao_atual = 0
        
        self.label_status.config(text=f"Memorize a sequência ({len(self.sequencia)} cores)...", 
                               fg='#3498db')
        
        # Desabilita botões durante a exibição
        for btn in self.botoes:
            btn.config(state='disabled')
        
        # Mostra a sequência
        self.mostrar_sequencia()
    
    def mostrar_sequencia(self):
        """Mostra a sequência de cores"""
        self.mostrando_sequencia = True
        
        def mostrar_cor(index):
            if not self.jogando or not self.mostrando_sequencia:
                return
                
            if index < len(self.sequencia):
                cor = self.sequencia[index]
                btn_index = self.cores.index(cor)
                
                # Acende a cor
                self.botoes[btn_index].config(relief='sunken', bd=8)
                self.root.update()
                
                velocidade = self.calcular_velocidade()
                
                # Programa para apagar a cor
                self.root.after(int(velocidade * 500), lambda: self.apagar_cor(btn_index))
                
                # Programa para mostrar a próxima cor
                self.root.after(int(velocidade * 1000), lambda: mostrar_cor(index + 1))
            else:
                # Terminou de mostrar a sequência
                self.mostrando_sequencia = False
                self.habilitar_botoes()
                self.label_status.config(text="Agora repita a sequência clicando nas cores!", 
                                       fg='#27ae60')
        
        # Inicia a exibição
        self.root.after(500, lambda: mostrar_cor(0))
    
    def apagar_cor(self, btn_index):
        """Apaga o destaque da cor"""
        if btn_index < len(self.botoes):
            self.botoes[btn_index].config(relief='raised', bd=4)
    
    def habilitar_botoes(self):
        """Habilita os botões para o jogador clicar"""
        for btn in self.botoes:
            btn.config(state='normal')
    
    def botao_clicado(self, cor):
        """Processa o clique em um botão de cor"""
        if not self.jogando or self.mostrando_sequencia:
            return
        
        self.entrada_jogador.append(cor)
        
        # Verifica se a cor está correta
        if cor == self.sequencia[self.posicao_atual]:
            self.posicao_atual += 1
            
            # Verifica se completou a sequência
            if self.posicao_atual == len(self.sequencia):
                self.pontuacao += 1
                self.atualizar_interface()
                
                # Desabilita botões
                for btn in self.botoes:
                    btn.config(state='disabled')
                
                # Verifica se aumentou a velocidade
                if self.pontuacao % 10 == 0:
                    self.label_status.config(text=f"🚀 NÍVEL UP! Pontuação: {self.pontuacao} - Velocidade aumentada!", 
                                           fg='#e74c3c')
                    # Som de nível up seria legal aqui
                else:
                    self.label_status.config(text=f"✅ Correto! Pontuação: {self.pontuacao}", 
                                           fg='#27ae60')
                
                # Próxima rodada após 2 segundos
                self.root.after(2000, self.proxima_rodada)
        else:
            # Erro - fim de jogo
            self.fim_de_jogo()
    
    def fim_de_jogo(self):
        """Processa o fim de jogo"""
        self.jogando = False
        
        for btn in self.botoes:
            btn.config(state='disabled')
        
        self.btn_novo_jogo.config(state='normal')
        self.btn_parar.config(state='disabled')
        
        self.label_status.config(text=f"❌ Game Over! Pontuação final: {self.pontuacao}", 
                               fg='#e74c3c')
        
        # Mostra mensagem de fim de jogo
        messagebox.showinfo("Fim de Jogo", 
                           f"🎮 Game Over!\n\n"
                           f"🏆 Pontuação Final: {self.pontuacao}\n"
                           f"⚡ Velocidade Final: {self.calcular_velocidade():.1f}s\n\n"
                           f"Parabéns pelo seu desempenho!")
    
    def atualizar_interface(self):
        """Atualiza as informações na interface"""
        self.label_pontuacao.config(text=f"PONTUAÇÃO: {self.pontuacao}")
        self.label_velocidade.config(text=f"VELOCIDADE: {self.calcular_velocidade():.1f}s")
    
    def executar(self):
        """Executa o jogo"""
        self.root.mainloop()

# Executa o jogo
if __name__ == "__main__":
    jogo = JogoDaMemoriaGUI()
    jogo.executar()