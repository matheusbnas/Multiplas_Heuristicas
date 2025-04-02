import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
import io
from PIL import Image
import time

class AnimatedKnightTour:
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.board = np.zeros((self.board_size, self.board_size))
        self.moves_history = []
        self.current_position = None
        self.unreachable_squares = []  # Novas casas não alcançáveis
        
    def create_board_image(self, current_pos=None, path=None):
        """Cria uma única imagem do tabuleiro"""
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Desenha o tabuleiro com letras e números nas bordas
        for i in range(self.board_size):
            for j in range(self.board_size):
                color = 'white' if (i + j) % 2 == 0 else 'lightgray'
                # Inverte o Y para desenhar o tabuleiro corretamente
                ax.add_patch(Rectangle((j, i), 1, 1, facecolor=color))
                
                # Adiciona letras (A-H) na parte inferior
                if i == 0:  # Primeira linha
                    ax.text(j + 0.5, -0.3, chr(65 + j), ha='center', va='center')
                # Adiciona números (1-8) na lateral
                if j == 0:
                    ax.text(-0.3, i + 0.5, str(1 + i), ha='center', va='center')
        
        # Desenha o caminho até a posição atual
        if path and len(path) > 1:
            path_array = np.array(path)
            # Converte as coordenadas para o sistema do tabuleiro
            plot_path = np.column_stack((path_array[:, 1], self.board_size - 1 - path_array[:, 0]))
            ax.plot(plot_path[:, 0] + 0.5, plot_path[:, 1] + 0.5, 
                   'b-', linewidth=2, alpha=0.5)
        
        # Marca as posições já visitadas
        if path:
            for idx, (x, y) in enumerate(path):
                # Converte as coordenadas para o sistema do tabuleiro
                ax.text(y + 0.5, (self.board_size - 1 - x) + 0.5, str(idx + 1), 
                       ha='center', va='center', fontsize=12)
        
        # Desenha o cavalo na posição atual
        if current_pos:
            x, y = current_pos
            # Converte as coordenadas para o sistema do tabuleiro
            ax.text(y + 0.5, (self.board_size - 1 - x) + 0.5, '♞', 
                   ha='center', va='center', color='black', fontsize=40)
        
        # Marca as casas não alcançáveis em vermelho
        for x, y in self.unreachable_squares:
            ax.add_patch(Rectangle((y, self.board_size - 1 - x), 1, 1, 
                        facecolor='red', alpha=0.3))
        
        ax.set_xlim(-0.5, self.board_size + 0.5)
        ax.set_ylim(-0.5, self.board_size + 0.5)
        plt.axis('off')
        
        # Converte a figura para imagem
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
        plt.close()
        buf.seek(0)
        return Image.open(buf)
    
    def create_animation(self, moves):
        """Cria uma sequência de imagens para a animação"""
        frames = []
        for i in range(len(moves)):
            img = self.create_board_image(moves[i], moves[:i+1])
            frames.append(img)
        return frames
    
    def get_valid_moves(self, position):
        """Retorna todos os movimentos válidos possíveis da posição atual"""
        x, y = position
        possible_moves = []
        moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.board_size and 0 <= new_y < self.board_size:
                if self.board[new_x, new_y] == 0:
                    possible_moves.append((new_x, new_y))
        
        return possible_moves
    
    def warnsdorff_next_move(self, position):
        """Implementa a heurística de Warnsdorff"""
        valid_moves = self.get_valid_moves(position)
        if not valid_moves:
            return None
        
        next_moves = []
        for move in valid_moves:
            self.board[move[0], move[1]] = 1
            num_next_moves = len(self.get_valid_moves(move))
            self.board[move[0], move[1]] = 0
            next_moves.append((num_next_moves, move))
        
        return min(next_moves, key=lambda x: x[0])[1]
    
    def solve_knights_tour(self, start_position):
        """Resolve o passeio do cavalo"""
        self.board = np.zeros((self.board_size, self.board_size))
        self.current_position = start_position
        self.board[start_position[0], start_position[1]] = 1
        self.moves_history = [start_position]
        
        while len(self.moves_history) < self.board_size * self.board_size:
            next_move = self.warnsdorff_next_move(self.current_position)
            if next_move is None:
                break
            
            self.current_position = next_move
            self.board[next_move[0], next_move[1]] = 1
            self.moves_history.append(next_move)
        
        return self.moves_history

    def find_unreachable_squares(self):
        """Identifica as casas não visitadas e verifica se são alcançáveis"""
        visited = set((x, y) for x, y in self.moves_history)
        unreachable = []
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (i, j) not in visited:
                    # Verifica se todas as casas vizinhas já foram visitadas
                    moves = self.get_valid_moves((i, j))
                    if not moves or all((x, y) in visited for x, y in moves):
                        unreachable.append((i, j))
        
        self.unreachable_squares = unreachable
        return unreachable

def main():
    st.title("Passeio do Cavalo Animado")
    
    # Explicação do sistema de coordenadas
    st.markdown("""
    ### Como usar:
    1. Escolha a posição inicial do cavalo usando as coordenadas X e Y:
       - X: coluna (0-7, da esquerda para direita)
       - Y: linha (0-7, de baixo para cima)
    2. Exemplo: (0,0) é o canto inferior esquerdo (A1 no xadrez)
    """)
    
    # Interface lateral
    st.sidebar.header("Configurações")
    
    # Atualiza o diagrama explicativo das coordenadas
    coord_explanation = """
    Sistema de Coordenadas:
    ```
    Y
    7  A8 B8 C8 D8 E8 F8 G8 H8
    6  A7 B7 C7 D7 E7 F7 G7 H7
    5  A6 B6 C6 D6 E6 F6 G6 H6
    4  A5 B5 C5 D5 E5 F5 G5 H5
    3  A4 B4 C4 D4 E4 F4 G4 H4
    2  A3 B3 C3 D3 E3 F3 G3 H3
    1  A2 B2 C2 D2 E2 F2 G2 H2
    0  A1 B1 C1 D1 E1 F1 G1 H1
       0  1  2  3  4  5  6  7  X
    ```
    """
    st.sidebar.markdown(coord_explanation)
    
    # Adiciona seleção de tamanho do tabuleiro
    board_size = st.sidebar.slider("Tamanho do tabuleiro:", min_value=8, max_value=16, value=8)
    
    # Adiciona seleção de heurística
    heuristic = st.sidebar.selectbox(
        "Escolha a heurística:",
        ["Warnsdorff", "Neural", "Backtracking", "Divide&Conquer"]
    )
    
    start_x = st.sidebar.selectbox("Posição inicial X (coluna):", range(board_size))
    start_y = st.sidebar.selectbox("Posição inicial Y (linha):", range(board_size))
    animation_speed = st.sidebar.slider("Velocidade da animação (ms)", 100, 1000, 500)
    
    if st.sidebar.button("Iniciar Passeio do Cavalo"):
        knight_tour = AnimatedKnightTour()
        
        # Converte as coordenadas para o sistema interno do tabuleiro
        start_position = (7 - start_y, start_x)  # Inverte o Y para corresponder ao tabuleiro
        
        # Resolve o passeio
        moves = knight_tour.solve_knights_tour(start_position)
        
        # Atualiza o texto mostrando a posição escolhida no formato de xadrez
        chess_column = chr(65 + start_x)  # Converte 0-7 para A-H
        chess_row = start_y + 1  # Converte 0-7 para 1-8
        st.write(f"Iniciando na posição: {chess_column}{chess_row} (X={start_x}, Y={start_y})")
        
        # Cria as imagens para animação
        frames = knight_tour.create_animation(moves)
        
        # Métricas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Casas visitadas", len(moves))
        with col2:
            coverage = (len(moves) / (knight_tour.board_size ** 2)) * 100
            st.metric("Cobertura do tabuleiro", f"{coverage:.1f}%")
        
        # Mostra a animação
        st.subheader("Animação do Passeio do Cavalo")
        placeholder = st.empty()
        
        while True:
            for frame in frames:
                placeholder.image(frame)
                time.sleep(animation_speed / 1000)
                
            time.sleep(1)
        
        # Após a animação, mostra o resumo das heurísticas
        st.markdown("""
        ### Explicação das Heurísticas
        
        1. **Heurística de Warnsdorff (1823)**
           - Escolhe sempre o próximo movimento que tem o menor número de saídas disponíveis
           - Simples e eficiente, mas pode falhar em alguns casos
           - Boa para tabuleiros menores
        
        2. **Heurística Neural**
           - Usa aprendizado de máquina para escolher os melhores movimentos
           - Mais adaptável a diferentes tamanhos de tabuleiro
           - Requer treinamento prévio
        
        3. **Heurística Backtracking**
           - Tenta todos os caminhos possíveis
           - Garante encontrar uma solução se existir
           - Mais lento em tabuleiros grandes
        
        4. **Heurística Divide&Conquer**
           - Divide o tabuleiro em regiões menores
           - Resolve cada região separadamente
           - Bom para tabuleiros grandes
        
        ### Estatísticas do Passeio
        - **Casas visitadas:** {len(moves)} de {board_size * board_size}
        - **Casas não alcançáveis:** {len(knight_tour.unreachable_squares)}
        - **Motivo das falhas:** Casas bloqueadas por movimentos anteriores
        """)
        
        # Mostra mapa de calor das casas mais visitadas
        #if st.checkbox("Mostrar mapa de calor de movimento"):
            # Código para gerar mapa de calor

if __name__ == "__main__":
    main()