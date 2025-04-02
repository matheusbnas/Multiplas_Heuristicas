# Projeto Passeio do Cavalo – Múltiplas Heurísticas

Este projeto implementa uma solução interativa para o problema do passeio do cavalo em tabuleiros de xadrez utilizando diferentes heurísticas, incluindo Warnsdorff, Neural, Backtracking, Divide & Conquer e AML (Accessibility and Move Length).

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

### 2. Heurística Neural
- **Princípio**: Utiliza múltiplos fatores para tomar decisões
- **Características consideradas**:
  - Acessibilidade da próxima posição
  - Distância do centro do tabuleiro
  - Distância das bordas
- **Vantagens**:
  - Boa adaptabilidade
  - Considera múltiplos fatores
- **Desvantagens**:
  - Mais complexa computacionalmente
  - Performance intermediária

### 3. Heurística Backtracking
- **Princípio**: Explora recursivamente todos os caminhos possíveis
- **Funcionamento**:
  - Testa diferentes sequências de movimentos
  - Retrocede quando encontra um caminho sem saída
- **Vantagens**:
  - Garante encontrar solução se existir
  - Solução ótima quando encontrada
- **Desvantagens**:
  - Tempo de execução exponencial
  - Inviável para tabuleiros grandes

### 4. Heurística Divide & Conquer
- **Princípio**: Divide o tabuleiro em quadrantes
- **Funcionamento**:
  - Balanceia movimentos entre diferentes regiões
  - Tenta manter opções em todas as áreas
- **Vantagens**:
  - Eficiente para tabuleiros grandes
  - Boa distribuição de movimento
- **Desvantagens**:
  - Pode ter problemas nas fronteiras
  - Performance pode variar

### 5. Heurística AML (Accessibility and Move Length)
- **Princípio**: Combina múltiplos critérios hierárquicos
- **Critérios em ordem de prioridade**:
  1. Regra de Warnsdorff (acessibilidade)
  2. Proximidade aos cantos do tabuleiro
  3. Proximidade às bordas
  4. Prioridade baseada na posição relativa
- **Vantagens**:
  - Muito consistente
  - Boa performance em diferentes tamanhos
- **Desvantagens**:
  - Mais complexa de implementar
  - Pode ser mais lenta que Warnsdorff

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
- Comparar o desempenho de todas as heurísticas
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

- Adição de novas heurísticas
- Suporte para tabuleiros maiores
- Interface interativa aprimorada
- Análise comparativa detalhada
- Visualização de casas não alcançáveis
