# Py-Runner 🦅

Um *endless runner* 2D em ritmo acelerado e com dificuldade progressiva, desenvolvido em **Python** e **Pygame-CE**. Corra, pule e deslize através de um mundo com rolagem infinita enquanto desvia de inimigos terrestres e aéreos.

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5.7-green.svg)
![Tests](https://img.shields.io/badge/Pytest-Coverage%2097%25-brightgreen)

---

## 🎮 Funcionalidades do Jogo

* **Dificuldade Progressiva:** O jogo é dividido em três fases consecutivas. Conforme você sobrevive por mais tempo, o motor global de rolagem do chão acelera levemente até culminar em sua velocidade máxima perigosa.
* **Física & Inércia ("Momentum"):** Controle seu personagem com configurações simuladas de peso e gravidade. Você pode saltar dos obstáculos, e utilizar a mecânica de *Fast-Fall* (Queda Rápida) para cortar velozmente a gravidade e deslizar instantaneamente por baixo de mosquitos aéreos que se aproximam.
* **Sistema de Pontuação de 3 Níveis:** Configuração global escalável entre 3 desafios (`Easy`, `Normal` e `Hard`). O Recorde de cada dificuldade é perfeitamente filtrado em listas puras localizadas através de um sistema unificado salvo pelo `config.json` no computador.
* **Ambiente em Paralaxe:** O fundo do seu Menu Principal roda nativamente a engine base desconectada, permitindo que imensas nuvens contornem sua vista suavemente no plano de fundo. Dentro da rotina do jogo, a terra entra no loop junto de uma nova textura, conectando as distâncias em um paralaxe belíssimo.
* **Opções Audiovisuais Persistentes:** O estado do jogo integra o *Mixer* para ler nativamente as Opções navegáveis pelo usuário, travando escolhas e o Volume Master.

## 🛠️ Instalação & Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/iamarangon/python-pygame-runner.git
   cd python-pygame-runner
   ```

2. **Crie um ambiente virtual (VENV - Recomendado):**
   ```bash
   python -m venv .venv
   
   # Windows:
   .\.venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Instale as Bibliotecas:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Importante: sempre prefira e confira se está baixando ativamente o pacote Community Edition - `pygame-ce` na documentação do projeto se houver problemas de execução de rotinas, ele melhora consideravelmente o suporte C+ interno para hardware).*

4. **Inicie sua rodada!**
   ```bash
   python main.py
   ```

---

## 🕹️ Controles Principais

| Ação | Tecla(s) |
| :--- | :--- |
| **Pular** | `Seta pra CIMA` (UP) ou `ESPAÇO` |
| **Abaixar / Queda Rápida** | `Seta pra BAIXO` (DOWN) |
| **Navegar nos Menus** | `CIMA` / `BAIXO` / `ESQUERDA` / `DIREITA` |
| **Confirmar Escolha** | `ENTER` ou `ESPAÇO` |
| **Limpar Tabelas e Pontuações** | `C` (Isso dentro da Tela Principal de Placar) |
| **Pausar e Beber Água** | `P` ou `ESC` (Isso ocorre apenas in-game) |

---

## 🧩 Arquitetura do Software

O **Py-Runner** se pauta com base nos padrões Orientados a Objetos construindo um clássico empilhamento comportamental ("State Machine"):
- **`src/core/game.py`**: A espinha central (App Loop) que re-escreve todos os nativos do backend `pygame.events` direcionando-os à classe atual.
- **`src/states/`**: A isolação real da UI de cada instante com vida própria de renderização (Menu, Configurações, Jogo, Game Over, Sistema de Nome...).
- **`src/core/resource_loader.py`**: Uma fábrica de carregamentos únicos instanciados (Singleton Cache). Nós lemos o seu HD lento exatas zero vezes durante o jogo! As texturas, sons e imagens PNG vão cruzar direto do seu arquivo binário pela máquina central subindo direto à sua Memória RAM. Sem lags!
- **`tests/`**: Como manda a segurança, criamos uma rede inteira programada e injetável baseada em testes contínuos usando Pytest+MockHeadless. Seu pipeline de Deploy no Git jamais colapsará por conta de colisões em ambiente hostless que chamem a interface preta `set_mode()`.

---

## 🚀 Próximos Passos (Refatoramento de Estrutura)

O próximo ciclo iminente de código (Sprint) prevê o re-alinhamento da forma como o laço (Collision vs Graphics) acontece mudando o patamar pra popular Estrutura Oficial Pygame **"ClearCode"**:
1. Portabilidade de todos scripts de atores (Entities) engatando eles estritamente como instâncias da classe nativa `pygame.sprite.Sprite`.
2. Absorção total da interface manual e dos arrays das *list_combos* delegando inteiramente o controle populacional e de exclusão da memória ao empilhador C `pygame.sprite.Group` para focar especificamente no draw() mais seguro.
3. Abandonar o cálculo de deltas contínuos customizados nas Spawns (calculando instantes de float-frame) pela pura interceptação nativa oficial ativando-se um `pygame.USEREVENT`. 

---

*Tenha uma ótima partida!*
<br>
**Criado por Italo Marangon.**
