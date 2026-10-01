# -*- coding: utf-8 -*-
"""
TASKTRACKER - Camada de Interface (CLI)
----------------------------------------
Responsável exclusivamente por entrada e saída de dados no terminal.
Não contém regras de negócio.
"""


def limpar_tela() -> None:
    """Limpa o terminal (compatível com Windows e Unix)."""
    import os
    os.system("cls" if os.name == "nt" else "clear")


def exibir_cabecalho() -> None:
    """Mostra o logotipo/marca do sistema."""
    print("=" * 60)
    print(r"  _____ _    _  _____ _  __ _____  ____   ____  _  __ _____ ____  ")
    print(r" |_   _/ \  | |/ /__ | |/ /_   _|  _ \ / ___|| |/ /| ____|  _ \ ")
    print(r"   | |/ _ \ | ' /  | | ' /  | | | |_) | |    | ' / |  _| | |_) |")
    print(r"   | / ___ \| . \  | | . \  | | |  _ <| |___ | . \ | |___|  _ < ")
    print(r"   |_/_/   \_\_|\_\ |_|_|\_\ |_| |_| \_\\____||_|\_\|_____|_| \_\\")
    print("=" * 60)
    print("        Gerenciador de Tarefas do Dia a Dia  •  v1.0")
    print("=" * 60)


def exibir_menu() -> None:
    """Exibe as opções disponíveis ao usuário."""
    print("\n┌──────────────────────────────────────────┐")
    print("│              MENU PRINCIPAL              │")
    print("├──────────────────────────────────────────┤")
    print("│  1 - Cadastrar tarefa                    │")
    print("│  2 - Visualizar tarefas pendentes        │")
    print("│  3 - Alterar tarefa                      │")
    print("│  4 - Excluir tarefa                      │")
    print("│  5 - Concluir tarefa                     │")
    print("│  6 - Visualizar histórico (concluídas)   │")
    print("│  7 - Sair                                │")
    print("└──────────────────────────────────────────┘")


def ler_opcao() -> str:
    """Lê a opção do menu digitada pelo usuário."""
    return input("👉 Escolha uma opção: ").strip()


def ler_texto(mensagem: str) -> str:
    """Wrapper de input para padronizar mensagens."""
    return input(mensagem).strip()


def pausar() -> None:
    """Aguarda o usuário pressionar ENTER para continuar."""
    input("\n⏎ Pressione ENTER para voltar ao menu...")


def exibir_mensagem(mensagem: str, tipo: str = "info") -> None:
    """Exibe mensagens padronizadas conforme o tipo."""
    icones = {
        "info": "ℹ️ ",
        "sucesso": "✅",
        "erro": "❌",
        "aviso": "⚠️ ",
    }
    print(f"{icones.get(tipo, '')} {mensagem}")


def exibir_tarefa(tarefa: dict, indice: int = None) -> None:
    """Formata a exibição de uma tarefa única."""
    prefixo = f"[{indice}] " if indice is not None else ""
    vencimento = tarefa.get("data_vencimento") or "sem data"
    print(f"  {prefixo}ID {tarefa['id']:>3} │ {tarefa['titulo']}")
    print(f"        Prioridade: {tarefa['prioridade']:<6} │ Vencimento: {vencimento}")


def exibir_tarefa_concluida(tarefa: dict) -> None:
    """Formata a exibição de uma tarefa do histórico."""
    print(f"  ✔️ ID {tarefa['id']:>3} │ {tarefa['titulo']}")
    print(f"        Concluída em: {tarefa['data_conclusao']} ({tarefa['dia_semana']})")
    print(f"        Prioridade:   {tarefa['prioridade']}")


---
