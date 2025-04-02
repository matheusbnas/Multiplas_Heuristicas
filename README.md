# Projeto Passeio do Cavalo – Heurística de Warnsdorff e Algoritmos Genéticos

Este projeto implementa uma solução interativa para o problema do passeio do cavalo em tabuleiros de xadrez utilizando a heurística de Warnsdorff. Além disso, o repositório reúne estudos e implementações complementares que exploram abordagens evolutivas (como algoritmos genéticos) para o mesmo problema.

## Visão Geral

- **Objetivo:** Demonstrar o uso da heurística de Warnsdorff para obter um passeio aberto do cavalo em tabuleiros quadrados, iniciando a partir de qualquer casa escolhida. Adicionalmente, o projeto explora abordagens alternativas baseadas em algoritmos genéticos, conforme apresentados nos PDFs incluídos.
- **Abordagem Principal:**  
  - **Warnsdorff:** A heurística determina o próximo movimento do cavalo escolhendo a casa com o menor número de movimentos válidos subsequentes. Essa estratégia visa evitar “becos sem saída” ao priorizar casas mais restritas.  
  - **Algoritmos Genéticos:** Em arquivos complementares, são apresentados estudos e implementações que aplicam técnicas evolutivas ao problema do passeio do cavalo, demonstrando a diversidade de abordagens de busca e otimização para este desafio clássico.
  
## Estrutura do Projeto

- **Código Fonte:**  
  - `chess_algoritmosgeneticos.py` – Contém a implementação interativa (usando Streamlit) do passeio do cavalo, com a visualização do tabuleiro e animação do percurso utilizando a heurística de Warnsdorff.  


- **Documentação e Estudos Teóricos:**  
  - `knightstour-SBPO.pdf` – Apresenta um estudo detalhado sobre heurísticas eficientes para o passeio aberto do cavalo a partir de casas arbitrárias, discutindo refinamentos na heurística de Warnsdorff.  
  
  - `mariaclicia,+4_Aplicação+de+Algoritmos+Genéticos+V.22.pdf` – Aborda a aplicação de algoritmos genéticos ao problema do passeio do cavalo, explicando a evolução dos indivíduos e o funcionamento dos operadores genéticos.
    
  - `algoritmogenetico-encoinfo2003.pdf` – Descreve uma implementação de algoritmo genético para o mesmo problema, ressaltando os conceitos de avaliação, mutação, cruzamento e seleção.
    

## Requisitos

- **Python 3.7+**
- **Bibliotecas Python:**  
  - `streamlit`
  - `numpy`
  - `matplotlib`
  - `PIL` (Pillow)
  
Para instalar as dependências, execute:
```bash
pip install streamlit numpy matplotlib pillow
```

## Como Executar

1. Clone o repositório para sua máquina local.
2. Instale as dependências conforme descrito na seção de requisitos.
3. Execute o aplicativo utilizando o Streamlit:
   ```bash
   streamlit run chess_algoritmosgeneticos.py
   ```
4. Na interface do aplicativo, escolha a posição inicial (coordenadas X e Y) e ajuste a velocidade da animação conforme desejado. Em seguida, clique em "Iniciar Passeio do Cavalo" para visualizar o percurso.

## Explicação Detalhada – Heurística de Warnsdorff

### Contexto e Problema

O problema do passeio do cavalo consiste em encontrar uma sequência de movimentos (passos em “L”) de modo que o cavalo visite cada casa de um tabuleiro exatamente uma vez. Trata-se de um problema clássico de caminho hamiltoniano em grafos, onde cada vértice (casa) é conectado aos outros através dos movimentos válidos do cavalo.

### A Heurística de Warnsdorff

Desenvolvida por H. C. Warnsdorff em 1823, a heurística baseia-se em uma estratégia gulosa: em cada movimento, o cavalo se desloca para a casa que tem o menor número de opções (movimentos válidos) para continuar o percurso. A ideia central é “atacar” as restrições antes que elas se agravem, evitando que o cavalo se isole em uma posição sem saída.

#### Passos da Heurística:

1. **Listar Movimentos Válidos:**  
   A partir da posição atual do cavalo, identifica-se todas as casas que ainda não foram visitadas e que podem ser alcançadas com um movimento em “L”.  
   (Conforme implementado em `get_valid_moves` no código.)
   
2. **Avaliação dos Próximos Movimentos:**  
   Para cada casa candidata, calcula-se o número de movimentos válidos que seriam possíveis se o cavalo se deslocasse para lá. Essa contagem é uma medida do “grau” da casa.
   
3. **Escolha do Movimento:**  
   Seleciona-se a casa com o menor grau – ou seja, a casa que oferece menos alternativas de continuação. Essa escolha tende a reduzir a probabilidade de o cavalo ficar preso sem opções futuras.  
   (A função `warnsdorff_next_move` no código exemplifica esse processo.)
   
4. **Iteração até Conclusão:**  
   O algoritmo repete o processo até que todas as casas tenham sido visitadas ou até que nenhum movimento válido seja encontrado.

### Vantagens e Limitações

- **Vantagens:**  
  - **Simplicidade e Eficiência:** A heurística é fácil de implementar e o tempo de execução cresce linearmente com o número de casas.
  - **Aplicabilidade em Vários Tamanhos:** Embora o método seja muito eficaz para tabuleiros convencionais (8×8), estudos estendidos mostram seu funcionamento para tabuleiros n×n com n variando a partir de casas arbitrárias.

- **Limitações:**  
  - **Casos de Falha:** Em alguns tabuleiros ou a partir de determinadas posições iniciais, a heurística pode não produzir um passeio completo, devido à natureza gulosa do método.
  - **Sensibilidade a Simetrias:** Algumas versões, como as discutidas no artigo de Álvarez-Martínez e Lázaro, podem apresentar resultados divergentes quando iniciadas de casas simétricas. Refinamentos que consideram a divisão do tabuleiro em octantes têm sido propostos para superar essa questão.

### Abordagens Complementares

Além da heurística de Warnsdorff, o projeto inclui referências a abordagens baseadas em algoritmos genéticos, onde uma população de soluções (representadas por cromossomos) evolui ao longo de gerações para maximizar a cobertura do tabuleiro. Esses métodos, embora geralmente mais lentos, oferecem um paradigma de busca global que pode ser útil quando a heurística gulosa não encontra uma solução.

## Conclusão

Este projeto demonstra de forma interativa como a heurística de Warnsdorff pode ser aplicada para resolver o clássico problema do passeio do cavalo a partir de qualquer casa inicial em tabuleiros quadrados. Ao mesmo tempo, os estudos presentes nos PDFs fornecem um panorama mais amplo das abordagens – tanto determinísticas quanto evolutivas – que podem ser utilizadas para explorar este desafio.
