
"""
Script final (v5) para avaliação de modelos Text-to-SQL no dataset Spider.

Esta versão utiliza a estrutura correta do objeto 'EvaluationResult' 
baseada na inspeção do ambiente do usuário, resolvendo os 'AttributeError'.
"""

import sqlite3
import json
import os
import argparse
import sys
from typing import List, Dict, Any

try:
    from deepeval.metrics import BaseMetric
    from deepeval.test_case import LLMTestCase
    from deepeval import evaluate
except ImportError:
    print("ERRO CRÍTICO: A biblioteca 'deepeval' não foi encontrada.")
    print("Por favor, instale-a com: pip install deepeval")
    sys.exit(1)


# Classe da Métrica de Execution Accuracy


class ExecutionAccuracyMetric(BaseMetric):
    """Métrica customizada para DeepEval que avalia a acurácia de execução de queries SQL."""
    def __init__(self, db_path: str, threshold: float = 1.0):
        self.db_path = db_path
        self.threshold = threshold
        super().__init__()

    def measure(self, test_case: LLMTestCase) -> float:
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            try:
                cursor.execute(test_case.actual_output)
                predicted_results = cursor.fetchall()
            except sqlite3.Error as e:
                self.reason = f"Sintaxe da query predita falhou: {e}"
                self.score = 0.0
                return self.score
            try:
                cursor.execute(test_case.expected_output)
                expected_results = cursor.fetchall()
            except sqlite3.Error as e:
                self.reason = f"Sintaxe da query esperada falhou: {e}"
                self.score = 0.0
                return self.score
            
            if set(predicted_results) == set(expected_results):
                self.score = 1.0
                self.reason = "Sucesso: Os resultados da execução são idênticos."
            else:
                self.score = 0.0
                self.reason = "Falha: Os resultados da execução são divergentes."
            return self.score
        except Exception as e:
            self.reason = f"Erro inesperado durante a medição: {e}"
            return 0.0
        finally:
            if conn:
                conn.close()

    async def a_measure(self, test_case: LLMTestCase) -> float:
        return self.measure(test_case)

    def is_successful(self) -> bool:
        return self.score >= self.threshold

# Funções Auxiliares

def load_data(file_path: str, is_jsonl: bool = False):
    """Carrega dados de um arquivo JSON ou JSONL."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if is_jsonl:
                results = {}
                for i, line in enumerate(f):
                    data = json.loads(line)
                    results[data.get('index', i)] = data.get('generated_sql', '').strip()
                return results
            else:
                return json.load(f)
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: Arquivo não encontrado em '{file_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"ERRO CRÍTICO: O arquivo '{file_path}' não é um JSON válido.")
        sys.exit(1)

def save_report(results: List[Dict], summary: Dict, output_file: str):
    """Salva o relatório em um arquivo JSON, criando o diretório se necessário."""
    try:
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"summary": summary, "detailed_results": results}, f, indent=4, ensure_ascii=False)
        print(f"\nRelatório de avaliação salvo com sucesso em '{output_file}'")
    except IOError as e:
        print(f"\nERRO: Não foi possível salvar o relatório em '{output_file}': {e}")

# Função Principal de Execução

def main():
    parser = argparse.ArgumentParser(description="Avaliador Text-to-SQL para o dataset Spider.")
    parser.add_argument("--results", required=True, help="Caminho para o arquivo .jsonl com os resultados do modelo.")
    parser.add_argument("--dev_file", required=True, help="Caminho para o arquivo dev.json do Spider.")
    parser.add_argument("--db_dir", required=True, help="Caminho para o diretório 'database' do Spider.")
    parser.add_argument("--output", required=True, help="Caminho para o arquivo JSON de saída do relatório.")
    args = parser.parse_args()

    print("1. Carregando dados...")
    dev_data = load_data(args.dev_file)
    model_results = load_data(args.results, is_jsonl=True)
    print(f"   - {len(dev_data)} exemplos carregados do dev set.")
    print(f"   - {len(model_results)} resultados do modelo carregados.")

    evaluation_report = []
    successful_count = 0
    total_evaluated_count = 0

    print("\n2. Iniciando processo de avaliação...")
    for index, item in enumerate(dev_data):
        db_id = item['db_id']
        generated_sql = model_results.get(index)
        db_path = os.path.join(args.db_dir, db_id, f"{db_id}.sqlite")

        if generated_sql is None or not generated_sql.strip() or not os.path.exists(db_path):
            continue

        total_evaluated_count += 1
        
      
        result = evaluate(
            test_cases=[LLMTestCase(input=item['question'], actual_output=generated_sql, expected_output=item['query'])],
            metrics=[ExecutionAccuracyMetric(db_path=db_path)]
        )
        
        test_case_result = result.test_results[0]
        metric_data = test_case_result.metrics_data[0]
        is_success = test_case_result.success
        
        if is_success:
            successful_count += 1
        
        evaluation_report.append({
            "index": index,
            "db_id": db_id,
            "question": item['question'],
            "expected_sql": item['query'],
            "generated_sql": generated_sql,
            "success": is_success,
            "score": metric_data.score,
            "reason": metric_data.reason
        })
        print(f"   - Itens avaliados: {total_evaluated_count}", end='\r')

    # Limpa a linha de progresso para a saída final
    print(f"                                           ", end='\r')
    print(f"3. Avaliação concluída.")
    
    summary = {
        "total_from_dev_set": len(dev_data),
        "total_from_model_results": len(model_results),
        "total_evaluated": total_evaluated_count,
        "total_successful": successful_count,
        "accuracy": (successful_count / total_evaluated_count) if total_evaluated_count > 0 else 0
    }

    print("\n Resumo da Avaliação")
    print(f"Total de Queries Avaliadas: {summary['total_evaluated']}")
    print(f"Queries Corretas: {summary['total_successful']}")
    print(f"Acurácia de Execução: {summary['accuracy']:.2%}")

    save_report(evaluation_report, summary, args.output)

if __name__ == '__main__':
    main()
