# -*- coding: utf-8 -*-
"""
TASKTRACKER - Testes Unitários
-------------------------------
Valida as regras de negócio definidas na Fase 1.
Execução: python -m unittest discover -s src/tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tarefas import (
    concluir_tarefa,
    criar_tarefa,
    normalizar_prioridade,
    ordenar_por_prioridade,
    validar_data,
    validar_prioridade,
    validar_titulo,
)


class TestValidarTitulo(unittest.TestCase):
    """RN01 - Título obrigatório."""

    def test_titulo_valido(self):
        self.assertTrue(validar_titulo("Estudar Python"))

    def test_titulo_vazio(self):
        self.assertFalse(validar_titulo(""))

    def test_titulo_apenas_espacos(self):
        self.assertFalse(validar_titulo("     "))

    def test_titulo_none(self):
        self.assertFalse(validar_titulo(None))


class TestValidarPrioridade(unittest.TestCase):
    """RN02 - Prioridade Alta/Média/Baixa."""

    def test_prioridades_validas(self):
        for p in ("Alta", "Média", "Baixa"):
            self.assertTrue(validar_prioridade(p), f"Falhou para {p}")

    def test_prioridade_minuscula(self):
        self.assertTrue(validar_prioridade("alta"))

    def test_prioridade_media_sem_acento(self):
        self.assertTrue(validar_prioridade("media"))

    def test_prioridade_invalida(self):
        self.assertFalse(validar_prioridade("Urgente"))

    def test_prioridade_vazia(self):
        self.assertFalse(validar_prioridade(""))


class TestNormalizarPrioridade(unittest.TestCase):
    def test_normaliza_media(self):
        self.assertEqual(normalizar_prioridade("media"), "Média")

    def test_normaliza_alta_maiuscula(self):
        self.assertEqual(normalizar_prioridade("ALTA"), "Alta")


class TestValidarData(unittest.TestCase):
    """RN03 - Data DD/MM/AAAA (opcional)."""

    def test_data_valida(self):
        self.assertTrue(validar_data("25/12/2026"))

    def test_data_vazia_permitida(self):
        self.assertTrue(validar_data(""))

    def test_data_formato_invalido(self):
        self.assertFalse(validar_data("2026-12-25"))

    def test_data_inexistente(self):
        self.assertFalse(validar_data("31/02/2026"))


class TestCriarTarefa(unittest.TestCase):
    """RN04 - Status inicial sempre 'Pendente'."""

    def test_status_inicial_pendente(self):
        tarefa = criar_tarefa("Lavar louça", "baixa", "")
        self.assertEqual(tarefa["status"], "Pendente")

    def test_prioridade_normalizada(self):
        tarefa = criar_tarefa("Estudar", "alta", "")
        self.assertEqual(tarefa["prioridade"], "Alta")

    def test_titulo_com_espacos_removidos(self):
        tarefa = criar_tarefa("   Comprar pão   ", "Média", "")
        self.assertEqual(tarefa["titulo"], "Comprar pão")

    def test_campos_de_historico_iniciais_vazios(self):
        tarefa = criar_tarefa("Teste", "Alta", "")
        self.assertEqual(tarefa["data_conclusao"], "")
        self.assertEqual(tarefa["dia_semana"], "")


class TestConcluirTarefa(unittest.TestCase):
    """RN05 - Registra data e dia da semana."""

    def test_status_muda_para_concluida(self):
        tarefa = criar_tarefa("Pagar contas", "Alta", "")
        concluir_tarefa(tarefa)
        self.assertEqual(tarefa["status"], "Concluída")

    def test_data_conclusao_preenchida(self):
        tarefa = criar_tarefa("Pagar contas", "Alta", "")
        concluir_tarefa(tarefa)
        self.assertRegex(tarefa["data_conclusao"], r"\d{2}/\d{2}/\d{4}")

    def test_dia_semana_valido(self):
        tarefa = criar_tarefa("Pagar contas", "Alta", "")
        concluir_tarefa(tarefa)
        self.assertIn(tarefa["dia_semana"], ("seg", "ter", "qua", "qui", "sex", "sab", "dom"))


class TestOrdenacao(unittest.TestCase):
    """Ordenação por prioridade."""

    def test_alta_vem_primeiro(self):
        tarefas = [
            criar_tarefa("Baixa", "Baixa", ""),
            criar_tarefa("Alta", "Alta", ""),
            criar_tarefa("Média", "Média", ""),
        ]
        ordenadas = ordenar_por_prioridade(tarefas)
        self.assertEqual([t["titulo"] for t in ordenadas], ["Alta", "Média", "Baixa"])


if __name__ == "__main__":
    unittest.main(verbosity=2)


---
