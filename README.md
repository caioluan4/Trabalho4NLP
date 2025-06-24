# Trabalho 4 de NLP: João Nogueira, Leonardo Irias, Caio Cunha

O repositório com os resultados do trabalho está estruturado da seguinte forma:

Na pasta `data` estão contidos arquivos importantes que foram utilizados no trabalho:
  1. na pasta `formatted_data`: os splits de treino e de teste (dev) do spider formatados com as consultas, o prompt few shot com 3 exemplos e o schema para construir as tabelas de cada exemplo
  2. na pasta `lora_adapter`: os dois adaptadores Lora gerados depois dos dois processos de treinamento no fine tuning
  3. na pasta `modelo_responses`: temos as respostas do modelo que foram utilizadas para a avaliação. Temos as respostas para SQL e MMLU dos modelos base e com adaptadores

Na pasta `scripts`estão contitos os códigos necessários para rodar todo o trabalho
  1. `fine_tuning_model.ipynb` contem a parte de fine tuning do modelo base (o Qlora1 e Qlora2)
  2. `gera_base_jsonl.jpynb` processo os dados de treino e dev do spider e coloca eles no formato necessário para treino e teste
  3. `testa_modelo_base_MMLU.ipynb` testa o modelo base nas questões do MMLU
  4. `testa_modelo_base_SQL testa` o modelo base nos exemplos do Spider
  5. `testa_modelo_lora_MMLU.ipynb` testa o modelo com os dois adaptadores nas questões do MMLU
  6. `testa_modelo_lora_SQL.ipynb` testa o modelo com os dois adaptadores nos exemplos do spider

Na pasta custom_metrics tempos salvo o arquivo `avaliador_spider.py`, que contem a métrica do spider implementada. Lá também estão os json com os resultados da avaliação na task de text-to-SQL

Checkpoint do modelo utilizado:
```
Remove inference parameters from README.md (#229)
8afb486
verified
vontimitta
Wauplin
HF Staff
```
