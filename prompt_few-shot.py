# NOTA: Substitua estes exemplos pelos 3 pares que você selecionar
# do training split do dataset Spider.
EXEMPLO_1_NL = "Quantos chefes de departamento têm mais de 55 anos de idade?"
EXEMPLO_1_SQL = "SELECT count(*) FROM head WHERE age > 55"

EXEMPLO_2_NL = "Liste os nomes dos departamentos em ordem alfabética."
EXEMPLO_2_SQL = "SELECT Dname FROM department ORDER BY Dname ASC"

EXEMPLO_3_NL = "Qual é o nome e o orçamento do departamento com o maior número de funcionários?"
EXEMPLO_3_SQL = "SELECT T2.dname, T2.budget FROM department_management AS T1 JOIN department AS T2 ON T1.department_id  =  T2.dept_id GROUP BY T1.department_id ORDER BY count(*) DESC LIMIT 1"

def prompt_few_shot(pergunta_nova: str) -> str:
    """
    Cria um prompt few-shot para a tarefa Text-to-SQL,
    incluindo 3 exemplos fixos para guiar o modelo.
    """
    # Este template deve ser fixo e usado em todas as avaliações de baseline 
    prompt = f"""Sua tarefa é converter perguntas em linguagem natural para consultas SQL. Siga os exemplos abaixo:

### Exemplo 1
Pergunta: {EXEMPLO_1_NL}
SQL:
{EXEMPLO_1_SQL}

### Exemplo 2
Pergunta: {EXEMPLO_2_NL}
SQL:
{EXEMPLO_2_SQL}

### Exemplo 3
Pergunta: {EXEMPLO_3_NL}
SQL:
{EXEMPLO_3_SQL}

### Pergunta para Converter
Pergunta: {pergunta_nova}
SQL:
"""
    return prompt

