# -*- coding: utf-8 -*-
"""
TASKTRACKER - Ponto de Entrada
-------------------------------
Contém o loop principal do sistema e orquestra as chamadas
entre a camada de interface (ui.menu) e as regras de negócio (tarefas).
"""

import os
import sys

# Garante que o diretório 'src' esteja no path ao executar diretamente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tarefas import (
    STATUS_CONCLUIDA,
    buscar_por_id,
    carregar_tarefas,
    concluir_tarefa,
    criar_tarefa,
    excluir_tarefa,
    gerar_proximo_id,
    listar_concluidas,
    listar_pendentes,
    normalizar_prioridade,
    salvar_tarefas,
    validar_data,
    validar_prioridade,
    validar_titulo,
)
from ui.menu import (
    exibir_cabecalho,
    exibir_mensagem,
    exibir_menu,
    exibir_tarefa,
    exibir_tarefa_concluida,
    ler_opcao,
    ler_texto,
    pausar,
)

# ---------------------------------------------------------------------------
# Funções auxiliares de entrada
# ---------------------------------------------------------------------------

def solicitar_titulo() -> str:
    """Insiste até que o usuário informe um título válido (RN01)."""
    while True:
        titulo = ler_texto("📝 Título da tarefa: ")
        if validar_titulo(titulo):
            return titulo
        exibir_mensagem("O título é obrigatório e não pode ficar em branco.", "erro")


def solicitar_prioridade() -> str:
    """Insiste até que o usuário informe uma prioridade válida (RN02)."""
    while True:
        prioridade = ler_texto("⚡ Prioridade (Alta / Média / Baixa): ")
        if validar_prioridade(prioridade):
            return normalizar_prioridade(prioridade)
        exibir_mensagem("Prioridade inválida. Use Alta, Média ou Baixa.", "erro")


def solicitar_data_vencimento() -> str:
    """Solicita data opcional no formato DD/MM/AAAA (RN03)."""
    while True:
        data = ler_texto("📅 Data de vencimento (DD/MM/AAAA) [ENTER para pular]: ")
        if validar_data(data):
            return data
        exibir_mensagem("Data inválida. Use o formato DD/MM/AAAA.", "erro")


def solicitar_id(mensagem: str = "🔎 Informe o ID da tarefa: "):
    """Lê um ID numérico. Retorna None se a entrada não for número."""
    entrada = ler_texto(mensagem)
    return int(entrada) if entrada.isdigit() else None


# ---------------------------------------------------------------------------
# Operações do menu
# ---------------------------------------------------------------------------

def opcao_cadastrar(tarefas: list) -> None:
    print("\n── CADASTRAR TAREFA ──")
    titulo = solicitar_titulo()
    prioridade = solicitar_prioridade()
    data_vencimento = solicitar_data_vencimento()

    nova = criar_tarefa(titulo, prioridade, data_vencimento)
    nova["id"] = gerar_proximo_id(tarefas)
    tarefas.append(nova)

    exibir_mensagem(f"Tarefa '{nova['titulo']}' cadastrada com sucesso! (ID {nova['id']})", "sucesso")


def opcao_visualizar(tarefas: list) -> None:
    print("\n── TAREFAS PENDENTES ──")
    pendentes = listar_pendentes(tarefas)

    if not pendentes:
        exibir_mensagem("Nenhuma tarefa pendente. Bom trabalho! 🎉", "aviso")
        return

    print(f"Total: {len(pendentes)} tarefa(s) pendente(s)\n")
    for indice, tarefa in enumerate(pendentes, start=1):
        exibir_tarefa(tarefa, indice)
    print()


def opcao_alterar(tarefas: list) -> None:
    print("\n── ALTERAR TAREFA ──")
    pendentes = listar_pendentes(tarefas)
    if not pendentes:
        exibir_mensagem("Não há tarefas pendentes para alterar.", "aviso")
        return

    for indice, tarefa in enumerate(pendentes, start=1):
        exibir_tarefa(tarefa, indice)

    id_tarefa = solicitar_id()
    tarefa = buscar_por_id(tarefas, id_tarefa) if id_tarefa else None

    if not tarefa:
        exibir_mensagem("Tarefa não encontrada.", "erro")
        return

    if tarefa["status"] == STATUS_CONCLUIDA:
        exibir_mensagem("Tarefas concluídas não podem ser alteradas (RN06).", "erro")
        return

    print(f"\nTarefa atual: {tarefa['titulo']}")
    print("(Pressione ENTER para manter o valor atual)\n")

    novo_titulo = ler_texto(f"📝 Novo título [{tarefa['titulo']}]: ")
    if novo_titulo and validar_titulo(novo_titulo):
        tarefa["titulo"] = novo_titulo

    nova_prioridade = ler_texto(f"⚡ Nova prioridade [{tarefa['prioridade']}]: ")
    if nova_prioridade:
        if validar_prioridade(nova_prioridade):
            tarefa["prioridade"] = normalizar_prioridade(nova_prioridade)
        else:
            exibir_mensagem("Prioridade inválida. Valor anterior mantido.", "aviso")

    nova_data = ler_texto(f"📅 Nova data [{tarefa['data_vencimento'] or 'sem data'}]: ")
    if nova_data:
        if validar_data(nova_data):
            tarefa["data_vencimento"] = nova_data
        else:
            exibir_mensagem("Data inválida. Valor anterior mantido.", "aviso")

    exibir_mensagem("Tarefa alterada com sucesso!", "sucesso")


def opcao_excluir(tarefas: list) -> None:
    print("\n── EXCLUIR TAREFA ──")
    pendentes = listar_pendentes(tarefas)
    if not pendentes:
        exibir_mensagem("Não há tarefas pendentes para excluir.", "aviso")
        return

    for indice, tarefa in enumerate(pendentes, start=1):
        exibir_tarefa(tarefa, indice)

    id_tarefa = solicitar_id()
    tarefa = buscar_por_id(tarefas, id_tarefa) if id_tarefa else None

    if not tarefa:
        exibir_mensagem("Tarefa não encontrada.", "erro")
        return

    if tarefa["status"] == STATUS_CONCLUIDA:
        exibir_mensagem("Tarefas concluídas não podem ser excluídas (RN06).", "erro")
        return

    confirmacao = ler_texto(f"⚠️  Confirma excluir '{tarefa['titulo']}'? (s/n): ").lower()
    if confirmacao == "s":
        excluir_tarefa(tarefas, id_tarefa)
        exibir_mensagem("Tarefa excluída com sucesso!", "sucesso")
    else:
        exibir_mensagem("Operação cancelada.", "info")


def opcao_concluir(tarefas: list) -> None:
    print("\n── CONCLUIR TAREFA ──")
    pendentes = listar_pendentes(tarefas)
    if not pendentes:
        exibir_mensagem("Não há tarefas pendentes para concluir.", "aviso")
        return

    for indice, tarefa in enumerate(pendentes, start=1):
        exibir_tarefa(tarefa, indice)

    id_tarefa = solicitar_id()
    tarefa = buscar_por_id(tarefas, id_tarefa) if id_tarefa else None

    if not tarefa or tarefa["status"] == STATUS_CONCLUIDA:
        exibir_mensagem("Tarefa não encontrada ou já concluída.", "erro")
        return

    concluir_tarefa(tarefa)
    exibir_mensagem(
        f"Tarefa concluída em {tarefa['data_conclusao']} ({tarefa['dia_semana']})! 🎉",
        "sucesso",
    )


def opcao_historico(tarefas: list) -> None:
    print("\n── HISTÓRICO DE TAREFAS CONCLUÍDAS ──")
    concluidas = listar_concluidas(tarefas)

    if not concluidas:
        exibir_mensagem("Nenhuma tarefa foi concluída ainda.", "aviso")
        return

    print(f"Total: {len(concluidas)} tarefa(s) concluída(s)\n")
    for tarefa in concluidas:
        exibir_tarefa_concluida(tarefa)
        print("  " + "-" * 50)
    print()


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------

def main() -> None:
    """Loop principal do TASKTRACKER."""
    tarefas = carregar_tarefas()

    while True:
        exibir_cabecalho()
        exibir_menu()
        opcao = ler_opcao()

        if opcao == "1":
            opcao_cadastrar(tarefas)
        elif opcao == "2":
            opcao_visualizar(tarefas)
        elif opcao == "3":
            opcao_alterar(tarefas)
        elif opcao == "4":
            opcao_excluir(tarefas)
        elif opcao == "5":
            opcao_concluir(tarefas)
        elif opcao == "6":
            opcao_historico(tarefas)
        elif opcao == "7":
            salvar_tarefas(tarefas)
            print("\n💾 Dados salvos. Obrigado por usar o TASKTRACKER! Até a próxima. 👋\n")
            break
        else:
            exibir_mensagem("Opção inválida. Digite um número de 1 a 7.", "erro")

        if opcao in ("1", "3", "4", "5"):
            salvar_tarefas(tarefas)

        pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execução interrompida pelo usuário. Saindo...\n")
        sys.exit(0)


---
