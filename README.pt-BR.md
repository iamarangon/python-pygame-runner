# Py-Runner 🦅

Um *endless runner* 2D com dificuldade progressiva, desenvolvido em **Python** e **Pygame-CE**.
Corra, pule e desvie de inimigos terrestres e aéreos num mundo com rolagem infinita.

![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)
![Pygame-CE](https://img.shields.io/badge/Pygame--CE-2.5.7-green.svg)
![Tests](https://img.shields.io/badge/Tests-80%20passando%20%7C%2096%25%20cobertura-brightgreen)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black)

---

## 🎮 Mecânicas do Jogo

- **3 Fases de Dificuldade Progressiva:** A velocidade de rolagem aumenta suavemente ao longo de três fases. Sobreviva o suficiente e o mundo se torna implacável.
- **Física & Inércia:** Pule, faça *Fast-Fall* no ar ou abaixe para desviar de inimigos aéreos. A gravidade é calibrada para um controle responsivo e satisfatório.
- **Placar de 3 Níveis:** Pontuações são registradas separadamente por dificuldade (`Easy`, `Normal`, `Hard`) e persistem entre sessões via `data/scores.json`.
- **Configurações Persistentes:** Volume e dificuldade são salvos automaticamente via `data/config.json`.
- **Ambiente em Paralaxe:** Rolagem infinita em dupla camada (céu e chão), com simulação de nuvens separada no menu principal.

---

## 🚀 Download & Jogar

> Baixe o executável mais recente para a sua plataforma diretamente na aba [**Releases**](../../releases) — sem precisar instalar Python.

| Plataforma | Arquivo |
|------------|---------|
| Windows    | `py-runner-windows.exe` |
| Linux      | `py-runner-linux` |
| macOS      | `py-runner-macos` |

---

## 🛠️ Executar pelo Código-Fonte

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/iamarangon/python-pygame-runner.git
   cd python-pygame-runner
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv .venv

   # Windows:
   .\.venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instale as dependências de execução:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jogar:**
   ```bash
   python main.py
   ```

---

## 🕹️ Controles

| Ação | Tecla(s) |
| :--- | :--- |
| **Pular** | `ESPAÇO` ou `↑` |
| **Abaixar / Queda Rápida** | `↓` |
| **Navegar nos Menus** | `↑` / `↓` / `←` / `→` |
| **Confirmar** | `ENTER` ou `ESPAÇO` |
| **Pausar** | `P` ou `ESC` |
| **Limpar Placar** | `C` (tela de Leaderboard) |

---

## 🧩 Arquitetura

| Camada | Descrição |
|--------|-----------|
| `main.py` | Ponto de entrada — inicializa o Pygame e inicia o loop |
| `src/core/game.py` | Loop central — roteia eventos para o State ativo |
| `src/states/` | Máquina de estados: Menu, Play, Pause, Game Over, Leaderboard, Options, Naming |
| `src/entities/` | Entidades baseadas em Sprite: `Player`, `Enemy`, `Background` |
| `src/core/spawner.py` | Injeta sprites de inimigos em Groups via timers `pygame.USEREVENT` |
| `src/core/resource_loader.py` | Cache Singleton — carrega imagens, sons e fontes uma única vez |
| `src/core/settings.py` | Constantes centrais: tela, física, dificuldade, timing |
| `tests/` | 80 testes headless, 96% de cobertura — compatível com CI sem display ou áudio |

---

## 🧪 Executar os Testes

```bash
pip install -r requirements-dev.txt
pytest --cov=src tests/
```

---

## 🙌 Créditos & Atribuições

A estrutura de código inicial deste projeto foi desenvolvida seguindo o excelente tutorial do canal do YouTube **Clear Code**.
- **Canal no YouTube:** [Clear Code](https://www.youtube.com/@ClearCode)
- **Link do Tutorial:** [The ultimate introduction to Pygame](https://www.youtube.com/watch?v=AY9MnQ4x3zk&list=PLsIbpk0M-XAlhSR7Bc6B7ef5h_PWkNA2B&index=1&t=2319s)

Todas as sprites e assets visuais utilizados neste projeto foram gentilmente disponibilizados no repositório dele.
- **Repositório do Projeto:** [UltimatePygameIntro](https://github.com/clear-code-projects/UltimatePygameIntro)
- **Perfil do Clear Code no GitHub:** [clear-code-projects](https://github.com/clear-code-projects)

---

*Boa sorte batendo o recorde!*
<br>
**Refatorado e Expandido por Italo Marangon.**
