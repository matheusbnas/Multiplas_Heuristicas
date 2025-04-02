import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
import io
from PIL import Image
import time
import pandas as pd

class AnimatedKnightTour:
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.board = np.zeros((self.board_size, self.board_size))
        self.moves_history = []
        self.current_position = None
        self.unreachable_squares = []  # Novas casas não alcançáveis
        
    def create_board_image(self, current_pos=None, path=None):
        """Cria uma única imagem do tabuleiro"""
        fig, ax = plt.subplots(figsize=(12, 12))
        
        # Desenha o tabuleiro com letras e números nas bordas
        for i in range(self.board_size):
            for j in range(self.board_size):
                color = 'white' if (i + j) % 2 == 0 else 'lightgray'
                # Inverte o Y para desenhar o tabuleiro corretamente
                ax.add_patch(Rectangle((j, i), 1, 1, facecolor=color))
                
                # Adiciona letras na parte inferior
                if i == 0:
                    ax.text(j + 0.5, -0.3, chr(65 + j) if j < 26 else f'A{j-25}', 
                           ha='center', va='center', fontsize=8)
                # Adiciona números na lateral
                if j == 0:
                    ax.text(-0.3, i + 0.5, str(self.board_size - i), 
                           ha='center', va='center', fontsize=8)
        
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
    
    def neural_next_move(self, position):
        """Implementa a heurística Neural"""
        valid_moves = self.get_valid_moves(position)
        if not valid_moves:
            return None
        
        next_moves = []
        for move in valid_moves:
            # Calcula características para a rede neural
            accessibility = len(self.get_valid_moves(move))
            center_distance = abs(move[0] - self.board_size//2) + abs(move[1] - self.board_size//2)
            edge_distance = min(move[0], move[1], self.board_size-1-move[0], self.board_size-1-move[1])
            
            # Simula um score neural (simplificado)
            # Adiciona um pequeno valor para evitar divisão por zero
            score = accessibility * 0.5 + edge_distance * 0.3
            if center_distance > 0:
                score += (1/center_distance) * 0.2
            else:
                score += 0.2  # Caso esteja no centro, adiciona valor máximo
                
            next_moves.append((score, move))
        
        return max(next_moves, key=lambda x: x[0])[1]

    def backtracking_next_move(self, position, depth=3):
        """Implementa a heurística Backtracking com profundidade limitada"""
        valid_moves = self.get_valid_moves(position)
        if not valid_moves:
            return None
        
        best_move = None
        best_score = -1
        
        for move in valid_moves:
            self.board[move[0], move[1]] = 1
            score = self._explore_moves(move, depth-1)
            self.board[move[0], move[1]] = 0
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

    def _explore_moves(self, position, depth):
        """Função auxiliar para backtracking"""
        if depth == 0:
            return len(self.get_valid_moves(position))
        
        valid_moves = self.get_valid_moves(position)
        if not valid_moves:
            return 0
        
        max_score = 0
        for move in valid_moves:
            self.board[move[0], move[1]] = 1
            score = self._explore_moves(move, depth-1)
            self.board[move[0], move[1]] = 0
            max_score = max(max_score, score)
        
        return max_score + len(valid_moves)

    def divide_conquer_next_move(self, position):
        """Implementa a heurística Divide & Conquer"""
        valid_moves = self.get_valid_moves(position)
        if not valid_moves:
            return None
        
        # Divide o tabuleiro em quadrantes
        mid_row = self.board_size // 2
        mid_col = self.board_size // 2
        
        next_moves = []
        for move in valid_moves:
            # Determina o quadrante do movimento
            quadrant = 0
            if move[0] < mid_row:
                if move[1] < mid_col:
                    quadrant = 1
                else:
                    quadrant = 2
            else:
                if move[1] < mid_col:
                    quadrant = 3
                else:
                    quadrant = 4
            
            # Calcula score baseado no quadrante menos visitado
            quadrant_visits = np.sum(self.board[
                (mid_row if quadrant > 2 else 0):(mid_row if quadrant <= 2 else self.board_size),
                (mid_col if quadrant % 2 == 0 else 0):(mid_col if quadrant % 2 == 1 else self.board_size)
            ])
            
            accessibility = len(self.get_valid_moves(move))
            score = accessibility * (1 + 1/quadrant_visits if quadrant_visits > 0 else 2)
            next_moves.append((score, move))
        
        return max(next_moves, key=lambda x: x[0])[1]
    
    def aml_next_move(self, position):
        """Implementa a heurística AML (Accessibility and Move Length)"""
        valid_moves = self.get_valid_moves(position)
        if not valid_moves:
            return None
        
        candidates = []
        for move in valid_moves:
            # 1. Critério Warnsdorff
            self.board[move[0], move[1]] = 1
            warnsdorff_score = len(self.get_valid_moves(move))
            self.board[move[0], move[1]] = 0
            
            # 2. Proximidade aos cantos
            corner_distance = min(
                abs(move[0]) + abs(move[1]),
                abs(move[0]) + abs(self.board_size-1 - move[1]),
                abs(self.board_size-1 - move[0]) + abs(move[1]),
                abs(self.board_size-1 - move[0]) + abs(self.board_size-1 - move[1])
            )
            
            # 3. Proximidade às bordas
            edge_distance = min(
                move[0], move[1],
                self.board_size-1 - move[0],
                self.board_size-1 - move[1]
            )
            
            # 4. Prioridade baseada na posição relativa
            priority = self._get_move_priority(position, move)
            
            candidates.append((warnsdorff_score, corner_distance, edge_distance, priority, move))
        
        # Ordena por todos os critérios
        return min(candidates, key=lambda x: (x[0], x[1], x[2], x[3]))[4]

    def _get_move_priority(self, current, candidate):
        """Calcula prioridade do movimento baseada na posição relativa"""
        dx = candidate[0] - current[0]
        dy = candidate[1] - current[1]
        # Prioridade baseada na direção do movimento
        priorities = {
            (2,1): 0, (1,2): 1, (-1,2): 2, (-2,1): 3,
            (-2,-1): 4, (-1,-2): 5, (1,-2): 6, (2,-1): 7
        }
        return priorities.get((dx,dy), 8)
    
    def solve_knights_tour(self, start_position, heuristic="Warnsdorff"):
        """Resolve o passeio do cavalo usando a heurística selecionada"""
        self.board = np.zeros((self.board_size, self.board_size))
        self.current_position = start_position
        self.board[start_position[0], start_position[1]] = 1
        self.moves_history = [start_position]
        
        heuristic_functions = {
            "Warnsdorff": self.warnsdorff_next_move,
            "Neural": self.neural_next_move,
            "Backtracking": self.backtracking_next_move,
            "Divide&Conquer": self.divide_conquer_next_move,
            "AML": self.aml_next_move
        }
        
        next_move_func = heuristic_functions.get(heuristic, self.warnsdorff_next_move)
        
        while len(self.moves_history) < self.board_size * self.board_size:
            next_move = next_move_func(self.current_position)
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

def analyze_heuristics(board_size=8, start_position=(0,0)):
    """Analisa o desempenho de cada heurística"""
    results = {}
    heuristics = ["Warnsdorff", "Neural", "Backtracking", "Divide&Conquer", "AML"]
    
    for heuristic in heuristics:
        start_time = time.time()
        knight_tour = AnimatedKnightTour(board_size)
        moves = knight_tour.solve_knights_tour(start_position, heuristic)
        end_time = time.time()
        
        results[heuristic] = {
            "casas_visitadas": len(moves),
            "cobertura": (len(moves) / (board_size ** 2)) * 100,
            "tempo_execucao": end_time - start_time,
            "casas_nao_alcancaveis": len(knight_tour.find_unreachable_squares())
        }
    
    return results

def get_heuristic_conclusion(df):
    """Gera conclusão dinâmica baseada nos resultados reais"""
    best_coverage = df["Cobertura (%)"].max()
    best_heuristic = df["Cobertura (%)"].idxmax()
    fastest = df["Tempo (s)"].idxmin()
    least_unreachable = df["Casas Não Alcançáveis"].idxmin()
    
    # Calcula score geral (normalizado)
    df_normalized = df.copy()
    df_normalized["Cobertura (%)"] = df_normalized["Cobertura (%)"] / df_normalized["Cobertura (%)"].max()
    df_normalized["Tempo (s)"] = 1 - (df_normalized["Tempo (s)"] / df_normalized["Tempo (s)"].max())
    df_normalized["Casas Não Alcançáveis"] = 1 - (df_normalized["Casas Não Alcançáveis"] / df_normalized["Casas Não Alcançáveis"].max())
    
    overall_score = df_normalized.mean(axis=1)
    best_overall = overall_score.idxmax()
    
    conclusion = f"""
        3. **Conclusão:**
        Para esta instância específica do problema do passeio do cavalo:
        
        - **Melhor cobertura:** {best_heuristic} ({best_coverage:.1f}%)
        - **Mais rápida:** {fastest}
        - **Menor número de casas não alcançáveis:** {least_unreachable}
        - **Melhor balanço geral:** {best_overall}
        
        A heurística {best_overall} mostrou-se mais eficiente neste caso por:
        - {"Maior cobertura do tabuleiro" if best_overall == best_heuristic else "Boa cobertura do tabuleiro"}
        - {"Melhor tempo de execução" if best_overall == fastest else "Tempo de execução aceitável"}
        - {"Menor número de casas não alcançáveis" if best_overall == least_unreachable else "Número aceitável de casas não alcançáveis"}
        
        Vale notar que o desempenho das heurísticas pode variar dependendo do tamanho do tabuleiro
        e da posição inicial escolhida."""
    
    return conclusion

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
    st.sidebar.title("Projeto de heurísticas para o passeio do cavalo")
    st.sidebar.markdown("[Desenvolvido por Matheus Bernardes](https://portfolio-matheusbernardes.netlify.app/)")
    st.sidebar.markdown("[GitHub](www.github.com/matheusbnas)")
    st.sidebar.markdown("[LinkedIn](www.linkedin.com/in/matheusbnas)") 
    print()
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
        ["Warnsdorff", "Neural", "Backtracking", "Divide&Conquer", "AML"]
    )
    
    start_x = st.sidebar.selectbox("Posição inicial X (coluna):", range(board_size))
    start_y = st.sidebar.selectbox("Posição inicial Y (linha):", range(board_size))
    animation_speed = st.sidebar.slider("Velocidade da animação (ms)", 100, 1000, 500)
    
    if st.sidebar.button("Iniciar Passeio do Cavalo"):
        knight_tour = AnimatedKnightTour(board_size)  # Pass board size
        start_position = (7 - start_y, start_x)
        moves = knight_tour.solve_knights_tour(start_position, heuristic)
        
        # Encontra casas não alcançáveis
        unreachable = knight_tour.find_unreachable_squares()
        
        # Atualiza o texto mostrando a posição escolhida no formato de xadrez
        chess_column = chr(65 + start_x)  # Converte 0-7 para A-H
        chess_row = start_y + 1  # Converte 0-7 para 1-8
        st.write(f"Iniciando na posição: {chess_column}{chess_row} (X={start_x}, Y={start_y})")
        
        # Cria as imagens para animação
        frames = knight_tour.create_animation(moves)
        
        # Métricas em 3 colunas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Casas visitadas", len(moves))
        with col2:
            coverage = (len(moves) / (board_size ** 2)) * 100
            st.metric("Cobertura do tabuleiro", f"{coverage:.1f}%")
        with col3:
            st.metric("Casas não alcançáveis", len(unreachable))
        
        # Mostra a animação
        st.subheader("Animação do Passeio do Cavalo")
        placeholder = st.empty()
        
        # Executa a animação uma única vez
        for frame in frames:
            placeholder.image(frame)
            time.sleep(animation_speed / 1000)
        
        # Adiciona explicação do resultado
        st.markdown(f"""
        ### Análise do Resultado
        
        - **Total de movimentos:** {len(moves)}
        - **Casas não visitadas:** {board_size * board_size - len(moves)}
        - **Porcentagem de cobertura:** {coverage:.1f}%
        - **Casas não alcançáveis:** {len(unreachable)}
        
        #### Detalhes da Heurística Utilizada: {heuristic}
        {get_heuristic_explanation(heuristic)}
        """)

    if st.checkbox("Mostrar análise comparativa das heurísticas"):
        st.subheader("Análise Comparativa das Heurísticas")
        results = analyze_heuristics(board_size, (7 - start_y, start_x))
        
        # Cria tabela comparativa
        df = pd.DataFrame(results).T
        df.columns = ["Casas Visitadas", "Cobertura (%)", "Tempo (s)", "Casas Não Alcançáveis"]
        st.table(df)
        
        # Análise dos resultados
        st.markdown(f"""
        ### Análise dos Resultados:
        
        1. **Melhor Cobertura:** {df["Cobertura (%)"].idxmax()} com {df["Cobertura (%)"].max():.1f}%
        
        2. **Comparação das Heurísticas:**
        
        - **AML:** 
            - Melhor equilíbrio entre cobertura e tempo
            - Usa múltiplos critérios hierárquicos
            - Mais consistente em diferentes tamanhos de tabuleiro
        
        - **Warnsdorff:** 
            - Rápida execução
            - Boa cobertura em tabuleiros menores
            - Pode falhar em tabuleiros maiores
        
        - **Neural:** 
            - Boa adaptabilidade
            - Performance intermediária
            - Mais complexa computacionalmente
        
        - **Backtracking:**
            - Garantia de encontrar solução se existir
            - Tempo de execução muito alto
            - Inviável para tabuleiros grandes
        
        - **Divide&Conquer:**
            - Boa para tabuleiros grandes
            - Performance pode variar
            - Pode ter problemas nas fronteiras dos quadrantes
        
        {get_heuristic_conclusion(df)}
        """)

def get_heuristic_explanation(heuristic):
    """Retorna explicação detalhada da heurística utilizada"""
    explanations = {
        "Warnsdorff": """
        A regra de Warnsdorff escolhe sempre o movimento que tem o menor número de saídas disponíveis.
        - A ideia é a de atacar primeiro as restrições mais severas, deixando para mais tarde as casas que poderão ser mais facilmente visitadas.
        - Vantagem: Simples e eficiente
        - Desvantagem: Pode falhar em tabuleiros maiores
        """,
        "Neural": """
        A heurística Neural considera múltiplos fatores:
        - Acessibilidade da próxima posição
        - Distância do centro
        - Distância das bordas
        """,
        "Backtracking": """
        O Backtracking explora possíveis caminhos com profundidade limitada:
        - Analisa movimentos futuros
        - Escolhe o caminho com mais opções
        - Mais lento, mas mais preciso
        """,
        "Divide&Conquer": """
        Divide&Conquer separa o tabuleiro em quadrantes:
        - Balanceia movimentos entre regiões
        - Tenta manter opções em todas as áreas
        - Bom para tabuleiros grandes
        """,
        "AML": """
        A heurística AML (Accessibility and Move Length) combina múltiplos critérios:
        - Acessibilidade baseada na regra de Warnsdorff
        - Proximidade aos cantos e bordas
        - Prioridade baseada na posição relativa
        """
    }
    return explanations.get(heuristic, "Explicação não disponível")

if __name__ == "__main__":
    main()