# Requisitos — TASKTRACKER

## 1. Requisitos Funcionais (RF)

| Código | Descrição |
|--------|-----------|
| RF01 | O sistema deve permitir cadastrar tarefas com título obrigatório |
| RF02 | O sistema deve permitir informar prioridade (Alta, Média, Baixa) |
| RF03 | O sistema deve permitir informar data de vencimento opcional (DD/MM/AAAA) |
| RF04 | O sistema deve listar tarefas pendentes ordenadas por prioridade |
| RF05 | O sistema deve permitir alterar tarefas pendentes |
| RF06 | O sistema deve permitir excluir tarefas pendentes |
| RF07 | O sistema deve permitir concluir tarefas, registrando data e dia da semana |
| RF08 | O sistema deve exibir histórico de tarefas concluídas |
| RF09 | O sistema deve persistir os dados em arquivo JSON |

## 2. Requisitos Não Funcionais (RNF)

| Código | Descrição |
|--------|-----------|
| RNF01 | Interface de linha de comando (CLI) simples e legível |
| RNF02 | Código modular (separação entre regras de negócio e interface) |
| RNF03 | Tratamento de exceções de entrada (não travar com dados inválidos) |
| RNF04 | Versionamento com Git seguindo commits semânticos |
| RNF05 | Cobertura mínima de testes unitários nas funções de validação |

## 3. Requisitos de Qualidade

- **Usabilidade:** menu numerado, mensagens claras de sucesso/erro.
- **Manutenibilidade:** funções pequenas e com responsabilidade única.
- **Confiabilidade:** validação em todas as entradas do usuário.
- **Rastreabilidade:** cada regra de negócio possui teste unitário correspondente.
