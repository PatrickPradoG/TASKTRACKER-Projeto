# -*- coding: utf-8 -*-
"""
TASKTRACKER - Módulo de Regras de Negócio
------------------------------------------
Concentra toda a lógica de manipulação das tarefas, validações
e persistência em arquivo JSON. Não possui dependência da interface.
"""

import json
import os
from datetime import datetime

# ---------------------------------------------------------------------------
# Constantes de configuração
# ---------------------------------------------------------------------------

RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_DADOS = os.path.join(RAIZ_PROJETO, "dados", "tarefas.json")

PRIORIDADES_VALIDAS = ("Alta", "Média", "Baixa")
PESO_PRIORIDADE = {"Alta": 1, "Média": 2, "Baixa": 3}
DIAS_SEMANA = ("seg", "ter", "qua", "qui", "sex", "sab", "dom")

STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"


# ---------------------------------------------------------------------------
# Validações (Regras de Negócio)
# ---------------------------------------------------------------------------

def validar_titulo(titulo: str) -> bool:
    """RN01 - O título é obrigatório e não pode conter apenas espaços."""
    return isinstance(titulo, str) and len(titulo.strip()) > 0


def validar_prioridade(prioridade: str) -> bool:
    """RN02 - Aceita exclusivamente Alta, Média ou Baixa."""
    if not isinstance(prioridade, str):
        return False
    return prioridade.strip().capitalize() in PRIORIDADES_VALIDAS


def normalizar_prioridade(prioridade: str) -> str:
    """Converte 'alta', 'ALTA', 'media' etc. para o padrão 'Alta'/'Média'/'Baixa'."""
    p = prioridade.strip().capitalize()
    if p == "Media":
        p = "Média"
    return p


def validar_data(data: str) -> bool:
    """RN03 - Valida o formato DD/MM/AAAA. String vazia é permitida (opcional)."""
    if data is None or data.strip() == "":
        return True  # campo opcional
    try:
        datetime.strptime(data.strip(), "%d/%m/%Y")
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Persistência
# ---------------------------------------------------------------------------

def carregar_tarefas() -> list:
    """Lê o arquivo JSON. Retorna lista vazia se não existir ou estiver corrompido."""
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
            return conteudo if isinstance(conteudo, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def salvar_tarefas(tarefas: list) -> None:
    """Grava a lista de tarefas em disco no formato JSON."""
    os.makedirs(os.path.dirname(ARQUIVO_DADOS), exist_ok=True)
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------

def gerar_proximo_id(tarefas: list) -> int:
    """Retorna o próximo ID sequencial disponível."""
    if not tarefas:
        return 1
    return max(tarefa.get("id", 0) for tarefa in tarefas) + 1


def criar_tarefa(titulo: str, prioridade: str, data_vencimento: str = "") -> dict:
    """
    Cria o dicionário de uma tarefa já validada.
    O status inicial é sempre 'Pendente' (RN04).
    """
    return {
        "id": 0,  # preenchido por quem chamar (main)
        "titulo": titulo.strip(),
        "prioridade": normalizar_prioridade(prioridade),
        "data_vencimento": data_vencimento.strip(),
        "status": STATUS_PENDENTE,
        "data_conclusao": "",
        "dia_semana": "",
    }


def buscar_por_id(tarefas: list, id_tarefa: int):
    """Retorna a tarefa com o ID informado ou None."""
    for tarefa in tarefas:
        if tarefa.get("id") == id_tarefa:
            return tarefa
    return None


def ordenar_por_prioridade(tarefas: list) -> list:
    """
    Ordena pendentes: primeiro por peso de prioridade (Alta<Média<Baixa),
    depois por data de vencimento (mais próxima primeiro).
    Tarefas sem data vão para o final do grupo.
    """
    def chave(tarefa):
        peso = PESO_PRIORIDADE.get(tarefa.get("prioridade", "Baixa"), 9)
        data = tarefa.get("data_vencimento", "")
        if data:
            try:
                data_ordem = datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                data_ordem = datetime.max
        else:
            data_ordem = datetime.max
        return (peso, data_ordem, tarefa.get("titulo", "").lower())

    return sorted(tarefas, key=chave)


def listar_pendentes(tarefas: list) -> list:
    """Filtra apenas tarefas com status Pendente, já ordenadas."""
    pendentes = [t for t in tarefas if t.get("status") == STATUS_PENDENTE]
    return ordenar_por_prioridade(pendentes)


def listar_concluidas(tarefas: list) -> list:
    """Retorna as tarefas concluídas ordenadas pela data de conclusão (mais recente primeiro)."""
    concluidas = [t for t in tarefas if t.get("status") == STATUS_CONCLUIDA]

    def chave(tarefa):
        try:
            return datetime.strptime(tarefa.get("data_conclusao", ""), "%d/%m/%Y")
        except ValueError:
            return datetime.min

    return sorted(concluidas, key=chave, reverse=True)


def concluir_tarefa(tarefa: dict) -> dict:
    """
    RN05 - Dá baixa na tarefa registrando data (dd/mm/aaaa)
    e dia da semana abreviado (seg, ter, qua, ...).
    """
    agora = datetime.now()
    tarefa["status"] = STATUS_CONCLUIDA
    tarefa["data_conclusao"] = agora.strftime("%d/%m/%Y")
    tarefa["dia_semana"] = DIAS_SEMANA[agora.weekday()]
    return tarefa


def excluir_tarefa(tarefas: list, id_tarefa: int) -> bool:
    """Remove a tarefa da lista. Retorna True se removeu."""
    for indice, tarefa in enumerate(tarefas):
        if tarefa.get("id") == id_tarefa:
            tarefas.pop(indice)
            return True
    return False


---
