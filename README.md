# TASKTRACKER-Projeto

# 📋 TASKTRACKER

Sistema de gerenciamento de tarefas do dia a dia, desenvolvido em **Python 3** com interface de linha de comando (CLI). Projeto acadêmico dividido em 3 fases: Planejamento, Implementação e Apresentação.

---

## 🎯 Objetivo

Auxiliar o usuário a **organizar sua rotina** e **otimizar o tempo**, permitindo cadastrar, alterar, excluir, consultar e concluir tarefas, além de manter um **histórico de conclusão** com data e dia da semana.

---

## ⚙️ Funcionalidades

| # | Funcionalidade | Descrição |
|---|----------------|-----------|
| 1 | Cadastrar tarefa | Título obrigatório, prioridade (Alta/Média/Baixa) e data de vencimento opcional |
| 2 | Visualizar pendentes | Lista ordenada por prioridade (Alta → Média → Baixa) |
| 3 | Alterar tarefa | Permite editar título, prioridade e data de vencimento |
| 4 | Excluir tarefa | Remove a tarefa com confirmação |
| 5 | Concluir tarefa | Dá baixa e registra data + dia da semana |
| 6 | Histórico | Lista tarefas concluídas com `dd/mm/aaaa` e `seg, ter, qua...` |
| 7 | Sair | Encerra o sistema salvando os dados |

---

## 🧠 Regras de Negócio

- **RN01** — Não é permitido cadastrar tarefa sem título (ou só com espaços).
- **RN02** — A prioridade aceita exclusivamente: `Alta`, `Média` ou `Baixa`.
- **RN03** — A data de vencimento, quando informada, deve estar no formato `DD/MM/AAAA` e ser válida.
- **RN04** — Toda tarefa criada recebe automaticamente o status `Pendente`.
- **RN05** — Ao concluir, o sistema registra `data_conclusao` (`dd/mm/aaaa`) e `dia_semana` (`seg`, `ter`, `qua`, `qui`, `sex`, `sab`, `dom`).
- **RN06** — Tarefas concluídas não podem ser editadas nem excluídas (integridade do histórico).

---

## 🛠️ Tecnologias

- Python 3.10+
- Git / GitHub
- JSON (persistência local)
- `unittest` (testes)

---

## ▶️ Como executar

bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/TASKTRACKER.git
cd TASKTRACKER

# 2. Execute a aplicação
python src/main.py

### Executar os testes

bash
python -m unittest discover -s src/tests -v

---

## 📂 Estrutura do Projeto


TASKTRACKER/
├── dados/                 # Persistência JSON (gerada automaticamente)
├── docs/                  # Documentação e planejamento
├── src/
│   ├── main.py            # Menu principal
│   ├── tarefas.py         # Regras de negócio
│   ├── ui/menu.py         # Interface CLI
│   └── tests/             # Testes unitários
├── README.md
└── requirements.txt

---

## 👤 Autor

**Patrick Prado Gonçalves** — Curso de [Tecnólogo em Análise e Desenvolvimento de Sistemas]
Projeto BOOTCAMP 2 — Fase 2 (Implementação e Git)
