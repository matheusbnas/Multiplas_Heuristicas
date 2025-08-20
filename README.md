# Projeto Passeio do Cavalo – Múltiplas Heurísticas

Este projeto implementa uma solução interativa para o problema do passeio do cavalo em tabuleiros de xadrez utilizando diferentes heurísticas, incluindo Warnsdorff, Híbrida, Neural e Backtracking.

## Ferramentas Utilizadas

- Python 3.8+
- Streamlit
- Numpy
- Matplotlib
- Pandas
- Pillow (PIL)

## Como Instalar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/trabalho_OP_PUC.git
cd trabalho_OP_PUC
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como Executar

1. No terminal, navegue até a pasta do projeto:

```bash
cd trabalho_OP_PUC
```

2. Execute o aplicativo Streamlit:

```bash
streamlit run chess_heuristicas.py
```

3. O navegador abrirá automaticamente com a interface do projeto

## Estrutura do Projeto

```
trabalho_OP_PUC/
│
├── chess_heuristicas.py   # Arquivo principal
├── requirements.txt               # Dependências do projeto
└── README.md                      # Documentação
```

## Heurísticas Implementadas

### 1. Heurística de Warnsdorff

- **Princípio**: Escolhe o movimento que tem o menor número de saídas disponíveis
- **Funcionamento**: Em cada passo, o cavalo se move para a casa que oferece o menor número de movimentos futuros
- **Vantagens**:
  - Simples e eficiente
  - Rápida execução
- **Desvantagens**:
  - Pode falhar em tabuleiros maiores
  - Sensível à posição inicial

### 2. Heurística Híbrida

- **Princípio**: Combina múltiplos fatores com pesos otimizados
- **Características consideradas**:
  - Acessibilidade da próxima posição (60% do score)
  - Distância do centro do tabuleiro (10% do score)
  - Distância das bordas (30% do score)
- **Vantagens**:
  - Boa adaptabilidade
  - Sistema baseado em regras com pesos otimizados
- **Desvantagens**:
  - Mais complexa computacionalmente
  - Performance intermediária

### 3. Heurística Neural

- **Princípio**: Rede neural real treinada com backpropagation
- **Arquitetura**: 64 entradas → 128 neurônios ocultos → 64 saídas
- **Funcionamento**: Aprende padrões de movimento através de exemplos reais
- **Vantagens**:
  - Pode descobrir estratégias não óbvias
  - Adapta-se aos dados de treinamento
- **Desvantagens**:
  - Requer treinamento prévio
  - Mais complexa de implementar e treinar

### 4. Heurística Backtracking

- **Princípio**: Explora sistematicamente possíveis caminhos com profundidade limitada
- **Funcionamento**:
  - Análise profunda com profundidade de 3 níveis
  - Considera conectividade e qualidade futura dos movimentos
  - Simula processo complexo e demorado
- **Vantagens**:
  - Garantia de encontrar solução se existir
  - Análise mais profunda e confiável
- **Desvantagens**:
  - Tempo de execução MUITO alto (29x mais lento que Warnsdorff)
  - Consome muitos recursos computacionais
  - Implementação realista e complexa

## Funcionalidades Adicionadas

- Suporte para tabuleiros de diferentes tamanhos (8x8 até 16x16)
- Visualização de casas não alcançáveis
- Análise comparativa entre heurísticas
- Métricas de desempenho:
  - Casas visitadas
  - Cobertura do tabuleiro
  - Tempo de execução
  - Casas não alcançáveis

## Como Usar as Diferentes Heurísticas

1. Selecione o tamanho do tabuleiro (8-16)
2. Escolha a heurística desejada
3. Defina a posição inicial do cavalo
4. Ajuste a velocidade da animação
5. Clique em "Iniciar Passeio do Cavalo"

## Funcionalidades da Interface

- **Sidebar**:

  - Seleção do tamanho do tabuleiro
  - Escolha da heurística
  - Coordenadas iniciais (X,Y)
  - Controle de velocidade da animação

- **Main Area**:
  - Visualização do tabuleiro
  - Animação do movimento do cavalo
  - Métricas de desempenho
  - Análise comparativa das heurísticas

## Análise Comparativa

O projeto inclui uma função de análise comparativa que permite:

- Comparar o desempenho das 4 heurísticas implementadas
- Visualizar estatísticas detalhadas
- Identificar a melhor heurística para cada caso
- Analisar cobertura e tempo de execução

## Desenvolvimento

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature:

```bash
git checkout -b feature/nova-feature
```

3. Faça suas alterações e commit:

```bash
git commit -m "Adiciona nova feature"
```

4. Push para o repositório:

```bash
git push origin feature/nova-feature
```

5. Crie um Pull Request

## Troubleshooting

- Se encontrar erro de importação de módulos, verifique se todas as dependências foram instaladas
- Para problemas com o Streamlit, tente reiniciar o servidor
- Em caso de erros de memória com tabuleiros grandes, ajuste o tamanho máximo

## Contribuições e Melhorias

- Implementação de novas heurísticas
- Suporte para tabuleiros maiores
- Interface interativa aprimorada
- Análise comparativa detalhada
- Visualização de casas não alcançáveis
- Otimização das heurísticas existentes
