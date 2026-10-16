# Mini DOOM — FPS retrô com raycasting em Python e Pygame

Projeto acadêmico desenvolvido para a disciplina de **Computação Gráfica**, ministrada pelo professor **Pedro Cândido**. O Mini DOOM é um jogo de ação e exploração em primeira pessoa, inspirado na estética dos FPS clássicos, criado com **Python 3** e **Pygame**.

Apesar da aparência tridimensional, o cenário é construído a partir de um **mapa bidimensional**. A técnica de **raycasting** projeta as paredes na tela, produzindo um efeito de perspectiva conhecido como *2.5D*. O projeto possui uma única fase em formato de labirinto.

- **Autor:** Paulo Melo
- **Disciplina:** Computação Gráfica
- **Professor:** Pedro Cândido
- **Repositório:** https://github.com/paulomelo0808/minidoom
- **Versão documentada:** versão funcional sem áudio, de outubro de 2026

## 1. Objetivo e regras

O jogador deve percorrer o labirinto, **encontrar uma chave** e **alcançar a saída** para concluir a fase. A saída só permite a vitória após a coleta da chave.

Durante a exploração, inimigos perseguem e atacam o jogador. A partida começa com **100 pontos de vida**; se a vida chegar a zero, ocorre a derrota. É possível iniciar uma nova partida após a vitória ou a derrota.

O desafio evolui com a geração periódica de inimigos: a fase começa com até três inimigos, e novos podem surgir a cada dez segundos, respeitando o limite de seis inimigos vivos e as regras de posicionamento. Quando o jogador coleta a chave, **novos inimigos deixam de ser gerados**.

## 2. Funcionalidades implementadas

- Visão em primeira pessoa construída com raycasting sobre um mapa 2D.
- Movimentação por teclado, orientação por mouse e colisões com paredes.
- Mapa superior em 2D, que pode ser exibido durante a partida.
- Pistola com mira, disparo, recuo, efeito visual e detecção de acerto.
- Inimigos representados por sprites escalados conforme a distância.
- Oclusão dos inimigos por paredes, com comparação de profundidade.
- Perseguição de inimigos por navegação em grade e cálculo de caminhos.
- Ataques dos inimigos, vida do jogador e HUD.
- Feedback visual: flash vermelho ao receber dano e piscadas claras nos inimigos atingidos.
- Chave coletável, indicador do objetivo, saída e telas de vitória e derrota.
- Menu principal, tela de controles, menu de pausa e reinício da partida.
- Geração progressiva de inimigos, interrompida após coletar a chave.

**Escopo atual:** uma fase, sem efeitos sonoros e sem sistema de salvamento ou pontuação persistente. O áudio está previsto como melhoria futura; **não é necessário para executar esta versão**.

## 3. Requisitos

- Python 3 (desenvolvimento e testes realizados com **Python 3.13.5**).
- Biblioteca **Pygame 2.6.1**, registrada em `requirements.txt`.
- Computador com ambiente gráfico e teclado/mouse.

O jogo foi desenvolvido e testado em **Debian Linux**. A execução em outros sistemas com Python e Pygame compatíveis é possível, mas não foi validada neste projeto.

## 4. Instalação e execução

No terminal, clone o projeto e entre no diretório:

```bash
git clone https://github.com/paulomelo0808/minidoom.git
cd minidoom
```

Crie e ative um ambiente virtual no Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale a dependência registrada:

```bash
python -m pip install -r requirements.txt
```

Inicie o jogo:

```bash
python main.py
```

Para sair do ambiente virtual após fechar o jogo:

```bash
deactivate
```

> **Importante:** execute `main.py` a partir da raiz do projeto. Não é necessário baixar modelos, imagens ou outros recursos durante a execução: os elementos gráficos desta versão são construídos pelo próprio código.

## 5. Controles

| Tecla ou ação | Função |
| --- | --- |
| `W`, `A`, `S`, `D` | Movimentar o jogador |
| Movimento do mouse | Alterar a direção da câmera |
| Clique esquerdo | Disparar a pistola |
| `Tab` | Alternar a visualização do mapa 2D |
| `Esc` (durante a partida) | Abrir o menu de pausa |
| `Esc` (durante a pausa) | Continuar a partida |
| `↑` / `↓` | Selecionar opções dos menus |
| `Enter` | Confirmar a opção selecionada |
| `R` (após vitória ou derrota) | Reiniciar a partida |
| `Esc` ou `Enter` (tela de controles) | Voltar ao menu principal |

No **menu de pausa**, também é possível selecionar **Continuar**, **Reiniciar partida** ou **Voltar ao menu**.

## 6. Técnicas de Computação Gráfica

### 6.1. Raycasting com DDA

O mapa é uma matriz de células: `1` representa uma parede e `0`, uma região transitável. Para cada direção amostrada no campo de visão, o algoritmo lança um raio a partir da posição do jogador e percorre a grade usando **DDA (*Digital Differential Analyzer*)** até encontrar uma parede. A distância obtida é utilizada para determinar a altura da faixa vertical projetada.

**Arquivos:** `mapa.py`, `raycasting.py` e `renderizador.py`.

### 6.2. Projeção em perspectiva e câmera

A projeção utiliza a distância perpendicular à direção da câmera para dimensionar as paredes e reduzir a distorção visual. A orientação da câmera é representada por um ângulo e atualizada pelo movimento horizontal do mouse. O campo de visão é configurado em `config.py`.

**Arquivos:** `main.py`, `config.py` e `renderizador.py`.

### 6.3. Sprites e oclusão por profundidade

Inimigos, chave e arma são desenhados com superfícies e primitivas do Pygame. Os sprites presentes no mundo são projetados e escalados conforme a distância. Para impedir que um inimigo apareça através de paredes, a renderização compara sua profundidade à profundidade das paredes em cada coluna visível.

**Arquivos:** `renderizador_inimigos.py`, `renderizador_chave.py`, `arma.py` e `renderizador.py`.

### 6.4. Composição por camadas e animação temporal

O jogo combina cenário, sprites, arma, mira, indicadores e interfaces por sobreposição de superfícies. Superfícies com transparência são utilizadas no menu de pausa e no efeito de dano. Temporizadores associados ao tempo entre quadros controlam os efeitos visuais, inclusive a alternância de cores dos inimigos atingidos.

**Arquivos:** `efeitos.py`, `menu.py`, `hud.py`, `main.py` e `renderizador_inimigos.py`.

## 7. Arquitetura do projeto

| Arquivo | Responsabilidade principal |
| --- | --- |
| `main.py` | Inicialização, laço principal, eventos, estados e integração dos sistemas |
| `config.py` | Resolução, FPS, velocidades, danos, limites e durações |
| `mapa.py` | Representação e posição inicial do labirinto |
| `raycasting.py` | Lançamento de raios e detecção de paredes por DDA |
| `renderizador.py` | Projeção do cenário em primeira pessoa e textura da saída |
| `jogador.py` | Movimentação do jogador |
| `colisoes.py` | Verificações espaciais e colisões |
| `arma.py` | Sprite da pistola, mira, recuo e efeitos de disparo |
| `inimigos.py` | Estados dos inimigos, perseguição, disparos e ataques |
| `navegacao.py` | Cálculo de caminhos no mapa |
| `renderizador_inimigos.py` | Projeção, profundidade e feedback visual dos inimigos |
| `spawn.py` | Posicionamento e geração periódica dos inimigos |
| `objetivos.py` | Coleta da chave e verificação da vitória |
| `renderizador_chave.py` | Projeção visual da chave |
| `hud.py` | Vida e telas de resultado |
| `menu.py` | Menu inicial, instruções e menu de pausa |
| `efeitos.py` | Efeito visual de dano recebido |
| `requirements.txt` | Dependências necessárias para execução |
| `README.md` | Instruções, descrição e documentação do projeto |

A lógica é organizada em módulos para separar movimentação, renderização, colisões, inteligência dos inimigos, objetivos e interface.

## 8. Desenvolvimento, testes e limitações

O desenvolvimento foi incremental, com checkpoints no histórico de commits. Entre os testes realizados durante a construção estão:

- Verificação da movimentação e das colisões no labirinto.
- Testes de disparo, dano, perseguição e eliminação de inimigos.
- Testes do sistema de geração de inimigos e da coleta da chave.
- Testes das condições de vitória, derrota e reinício.
- Testes dos menus, da pausa e da retomada da partida.
- Correção dos temporizadores dos efeitos visuais, para que fossem atualizados independentemente uns dos outros.
- Verificações de sintaxe com `python -m compileall -q`.

**Limitações conhecidas:** o jogo contém somente uma fase; não há áudio nem persistência de partidas; a dificuldade é definida por constantes e pela progressão de inimigos. A estabilidade foi verificada durante os testes locais, não por uma campanha automatizada abrangente em múltiplos sistemas operacionais.

A evolução do trabalho pode ser consultada no [histórico de commits do repositório](https://github.com/paulomelo0808/minidoom/commits/main).

## 9. Créditos, referências e uso de inteligência artificial

**Desenvolvimento acadêmico:** Paulo Melo, na disciplina de Computação Gráfica do professor Pedro Cândido.

**Tecnologias:**

- [Python](https://www.python.org/) — linguagem de programação.
- [Pygame](https://www.pygame.org/docs/) — biblioteca para janela, entrada de dados, superfícies, desenho e controle do tempo.

**Referência estética:** jogos de tiro clássicos em primeira pessoa, especialmente *DOOM*, como inspiração de gênero e apresentação visual. O Mini DOOM é um projeto didático independente, sem afiliação com os titulares da marca.

**Recursos gráficos:** sprites e interfaces desenhados por código com primitivas e superfícies do Pygame; esta versão não depende de pacotes externos de imagens ou áudio.

**Uso de IA:** o **ChatGPT (OpenAI)** foi utilizado como ferramenta de apoio ao planejamento, estudo de conceitos (incluindo raycasting e projeção), elaboração e revisão de trechos de código, diagnóstico de erros, organização da implementação e documentação. As sugestões foram integradas progressivamente, executadas e verificadas localmente pelo responsável pelo projeto. O uso da ferramenta não substitui a responsabilidade de compreender, testar e explicar o código entregue.

O código-fonte e os registros de desenvolvimento estão disponíveis no repositório indicado acima.

---

**Mini DOOM — Projeto acadêmico de Computação Gráfica — 2026.**
