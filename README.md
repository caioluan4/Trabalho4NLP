# Trabalho 4 de NLP: João Nogueira, Leonardo Irias, Caio Cunha

O repositório com os resultados do trabalho está estruturado da seguinte forma:

Na pasta `data` estão contidos arquivos importantes que foram utilizados no trabalho:
  1. na pasta `formatted_data`: os splits de treino e de teste (dev) do spider formatados com as consultas, o prompt few shot com 3 exemplos e o schema para construir as tabelas de cada exemplo
  2. na pasta `lora_adapter`: os dois adaptadores Lora gerados depois dos dois processos de treinamento no fine tuning
  3. na pasta `modelo_responses`: temos as respostas do modelo que foram utilizadas para a avaliação. Temos as respostas para SQL e MMLU dos modelos base e com adaptadores
