# 🧠 Rede Neural para o Problema do Passeio do Cavalo

## 📋 Visão Geral

Este documento descreve a implementação de uma **rede neural real com backpropagation** para resolver o problema do passeio do cavalo em tabuleiros de xadrez. A rede neural aprende padrões de movimento através de exemplos de jogos bem-sucedidos.

## 🏗️ Arquitetura da Rede Neural

### Estrutura das Camadas

```
Entrada: 64 neurônios (8x8 posições do tabuleiro)
    ↓
Camada Oculta: 128 neurônios com ativação sigmoid
    ↓
Saída: 64 neurônios (probabilidade de cada movimento)
```

### Parâmetros da Rede

- **Entrada**: 64 dimensões (tabuleiro 8x8)
- **Camada Oculta**: 128 neurônios
- **Saída**: 64 dimensões
- **Função de Ativação**: Sigmoid
- **Inicialização**: Pesos pequenos aleatórios (±0.01)

## 🔧 Componentes Técnicos

### 1. Função Sigmoid

```python
def sigmoid(self, x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
```

**O que é Sigmoid?**

- **Função de ativação** que transforma qualquer número em um valor entre 0 e 1
- **Formato**: S-shaped (curva em S)
- **Fórmula**: σ(x) = 1 / (1 + e^(-x))

**Por que Sigmoid?**

- **Normaliza** saídas para probabilidades (0-1)
- **Suave** e diferenciável (importante para backpropagation)
- **Não-linearidade** que permite à rede aprender padrões complexos

**Exemplos de Valores:**

- sigmoid(0) = 0.5
- sigmoid(5) ≈ 0.993
- sigmoid(-5) ≈ 0.007

### 2. Derivada da Sigmoid

```python
def sigmoid_derivative(self, x):
    return x * (1 - x)
```

**O que é a Derivada?**

- **Taxa de mudança** da função sigmoid
- **Usada no backpropagation** para calcular gradientes
- **Fórmula**: σ'(x) = σ(x) × (1 - σ(x))

**Por que é Importante?**

- **Gradiente descendente** precisa saber como ajustar pesos
- **Derivada** indica a direção e magnitude da mudança
- **Sem derivada**, não é possível treinar a rede

## 🎯 Representação dos Dados

### Vetor de Entrada (64 dimensões)

```python
def _position_to_input_vector(self, position):
    input_vector = np.zeros(64)  # 8x8 = 64 posições

    # Posição atual: valor 1.0
    x, y = position
    input_vector[x * 8 + y] = 1.0

    # Casas visitadas: valor 0.5
    for visited_x, visited_y in self.moves_history:
        if 0 <= visited_x < 8 and 0 <= visited_y < 8:
            input_vector[visited_x * 8 + visited_y] = 0.5

    # Movimentos possíveis: valor 0.3
    for dx, dy in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8 and self.board[new_x, new_y] == 0:
            input_vector[new_x * 8 + new_y] = 0.3

    return input_vector
```

**Estrutura do Vetor:**

- **Posição 0-63**: Representa cada casa do tabuleiro (0,0) a (7,7)
- **Valor 1.0**: Posição atual do cavalo
- **Valor 0.5**: Casas já visitadas
- **Valor 0.3**: Movimentos possíveis do cavalo
- **Valor 0.0**: Casas não acessíveis ou irrelevantes

### Vetor de Saída (64 dimensões)

```python
def _move_to_target_vector(self, move):
    target = np.zeros(64)
    x, y = move
    target[x * 8 + y] = 1  # Movimento correto
    return target
```

**Estrutura do Vetor Alvo:**

- **Valor 1.0**: Movimento correto (usando Warnsdorff como referência)
- **Valor 0.0**: Todos os outros movimentos

## 🚀 Algoritmo de Treinamento

### 1. Forward Propagation

```python
def forward(self, X):
    # Camada oculta
    self.hidden = self.sigmoid(np.dot(X, self.weights1) + self.bias1)

    # Camada de saída
    self.output = self.sigmoid(np.dot(self.hidden, self.weights2) + self.bias2)

    return self.output
```

**O que Acontece:**

1. **Entrada × Pesos1 + Bias1** → Camada oculta
2. **Aplica sigmoid** na camada oculta
3. **Oculta × Pesos2 + Bias2** → Camada de saída
4. **Aplica sigmoid** na saída
5. **Retorna** predição final

### 2. Backpropagation

```python
def backward(self, X, y, learning_rate=0.01):
    m = X.shape[0]  # Número de exemplos

    # Calcula gradientes
    d_output = (self.output - y) * self.sigmoid_derivative(self.output)
    d_hidden = np.dot(d_output, self.weights2.T) * self.sigmoid_derivative(self.hidden)

    # Atualiza pesos e bias
    self.weights2 -= learning_rate * np.dot(self.hidden.T, d_output) / m
    self.bias2 -= learning_rate * np.mean(d_output, axis=0)
    self.weights1 -= learning_rate * np.dot(X.T, d_hidden) / m
    self.bias1 -= learning_rate * np.mean(d_hidden, axis=0)
```

**O que Acontece:**

1. **Calcula erro** entre predição e resposta correta
2. **Propaga erro** de volta pelas camadas
3. **Calcula gradientes** para cada peso
4. **Atualiza pesos** na direção que reduz o erro

### 3. Treinamento em Batches

```python
def train(self, X, y, epochs=100, learning_rate=0.01, batch_size=32):
    for epoch in range(epochs):
        # Shuffle dos dados
        indices = np.random.permutation(len(X))
        X_shuffled = X[indices]
        y_shuffled = y[indices]

        # Treinamento em batches
        for i in range(0, len(X), batch_size):
            batch_X = X_shuffled[i:i+batch_size]
            batch_y = y_shuffled[i:i+batch_size]

            # Forward + Backward
            self.forward(batch_X)
            self.backward(batch_X, batch_y, learning_rate)
```

**Vantagens dos Batches:**

- **Estabilidade** no treinamento
- **Eficiência** computacional
- **Melhor generalização**
- **Evita overfitting**

## 📊 Geração de Dados de Treinamento

### Estratégia de Treinamento

```python
def _generate_training_data(self, num_games=1000):
    training_data = []
    target_moves = []

    for game in range(num_games):
        # Reseta tabuleiro para novo jogo
        self.board = np.zeros((8, 8))
        self.moves_history = []

        # Joga usando Warnsdorff como "professor"
        start_pos = (np.random.randint(0, 8), np.random.randint(0, 8))
        # ... joga jogo completo ...

        # Adiciona dados de treinamento
        if len(self.moves_history) > 1:
            input_vector = self._position_to_input_vector(self.moves_history[-2])
            target_vector = self._move_to_target_vector(next_move)

            training_data.append(input_vector)
            target_moves.append(target_vector)
```

**Por que Warnsdorff como Professor?**

- **Algoritmo comprovado** que funciona bem
- **Gera jogos válidos** e bem-sucedidos
- **Fornece exemplos de qualidade** para aprendizado
- **Base sólida** para a rede neural aprender

## 🎮 Como a Rede Neural Faz Predições

### 1. Conversão de Entrada

```python
def neural_next_move(self, position):
    # Converte posição atual em vetor de entrada
    input_vector = self._position_to_input_vector(position)

    # Faz predição da rede neural
    prediction = self.neural_network.predict(input_vector)

    # Encontra melhor movimento baseado na predição
    best_move = None
    best_score = -float('inf')

    for move in valid_moves:
        move_score = self._calculate_move_score(move, prediction)
        if move_score > best_score:
            best_score = move_score
            best_move = move

    return best_move
```

### 2. Cálculo de Score

```python
def _calculate_move_score(self, move, prediction):
    x, y = move

    # Score base da predição da rede
    base_score = prediction[x * 8 + y]

    # Bonus para movimentos que mantêm opções futuras
    self.board[x, y] = 1
    future_moves = len(self.get_valid_moves(move))
    self.board[x, y] = 0

    # Score composto: predição da rede + heurística de acessibilidade
    final_score = base_score * 0.7 + (future_moves / 8.0) * 0.3

    return final_score
```

**Score Composto:**

- **70%**: Predição da rede neural (aprendizado)
- **30%**: Heurística de acessibilidade (regra tradicional)

## 🔍 Hiperparâmetros e Configurações

### Parâmetros de Treinamento

- **Épocas**: 100 (número de passadas completas pelos dados)
- **Taxa de Aprendizado**: 0.01 (velocidade de ajuste dos pesos)
- **Tamanho do Batch**: 32 (exemplos processados por vez)
- **Jogos de Treinamento**: 1000 (dados de treinamento)

### Inicialização dos Pesos

```python
# Pesos pequenos para evitar saturação da sigmoid
self.weights1 = np.random.randn(input_size, hidden_size) * 0.01
self.weights2 = np.random.randn(hidden_size, output_size) * 0.01

# Bias inicializado em zero
self.bias1 = np.zeros(hidden_size)
self.bias2 = np.zeros(output_size)
```

## 📈 Métricas de Performance

### Loss Function (Função de Perda)

```python
def calculate_loss(self, X, y):
    predictions = self.forward(X)
    return np.mean((predictions - y) ** 2)  # Erro quadrático médio
```

**Interpretação:**

- **Loss = 0**: Predição perfeita
- **Loss = 1**: Predição completamente errada
- **Objetivo**: Minimizar loss durante treinamento

### Histórico de Treinamento

```python
# A cada 10 épocas
if epoch % 10 == 0:
    loss = self.calculate_loss(X, y)
    self.training_history.append(loss)
    print(f"Época {epoch}, Loss: {loss:.6f}")
```

## 🚧 Limitações e Considerações

### 1. Overfitting

- **Risco**: Rede memoriza dados de treinamento
- **Solução**: Validação cruzada, early stopping
- **Monitoramento**: Loss de validação vs. treinamento

### 2. Dependência dos Dados

- **Qualidade**: Depende da qualidade dos jogos de Warnsdorff
- **Quantidade**: Mais dados = melhor aprendizado
- **Variedade**: Diferentes posições iniciais importantes

### 3. Interpretabilidade

- **Black box**: Difícil entender por que rede escolhe movimento
- **Debugging**: Complexo de debugar decisões incorretas
- **Explicabilidade**: Área de pesquisa ativa

## 🔮 Melhorias Futuras

### 1. Arquitetura da Rede

- **Mais camadas**: Rede mais profunda
- **Dropout**: Regularização para evitar overfitting
- **Batch Normalization**: Estabilização do treinamento
- **Ativações alternativas**: ReLU, Leaky ReLU

### 2. Otimização

- **Adam/SGD**: Otimizadores mais avançados
- **Learning Rate Scheduling**: Taxa de aprendizado adaptativa
- **Early Stopping**: Parada automática quando overfitting
- **Cross-validation**: Validação mais robusta

### 3. Dados de Treinamento

- **Auto-gerados**: Rede gera seus próprios dados
- **Reinforcement Learning**: Aprende jogando contra si mesma
- **Transfer Learning**: Usa conhecimento de outros problemas
- **Data Augmentation**: Variações dos dados existentes

### 4. Avaliação

- **Métricas múltiplas**: Acurácia, precisão, recall
- **Comparação com heurísticas**: Benchmarking
- **Análise de erros**: Por que rede falha
- **Visualização**: Gráficos de decisão

## 📚 Referências Técnicas

### Conceitos Fundamentais

- **Gradiente Descendente**: Otimização de funções
- **Regra da Cadeia**: Cálculo de derivadas
- **Funções de Ativação**: Sigmoid, ReLU, Tanh
- **Regularização**: Dropout, L1/L2, Early Stopping

### Algoritmos Relacionados

- **Q-Learning**: Aprendizado por reforço
- **Genetic Algorithms**: Otimização evolutiva
- **Monte Carlo Tree Search**: Exploração de árvores
- **AlphaZero**: Combinação de RL e redes neurais

## 🎯 Conclusão

A implementação da rede neural para o problema do passeio do cavalo representa uma abordagem **híbrida** que combina:

1. **Aprendizado automático** através de backpropagation
2. **Heurísticas tradicionais** como base de conhecimento
3. **Representação estruturada** do problema do xadrez
4. **Treinamento supervisionado** com dados de qualidade

Esta implementação serve como **base sólida** para experimentos futuros e demonstra como **redes neurais clássicas** podem ser aplicadas a problemas de **otimização combinatória**.

---

_Documento criado para facilitar compreensão e melhorias futuras da implementação da rede neural para o problema do passeio do cavalo._
