# 🏥 Self-Healing Data Pipeline com Agentes Autônomos (DataOps)

Este projeto demonstra a construção de uma **Pipeline de Dados Resiliente (Self-Healing)** capaz de lidar com anomalias de tipagem e dados corrompidos de forma autônoma. 

A arquitetura utiliza **Polars** para processamento ultrarrápido e **Ollama** para rodar um LLM (Large Language Model) 100% localmente. O agente atua como um engenheiro de DataOps: ao detectar uma falha na ingestão do lote, ele isola as linhas defeituosas (Quarentena), recupera os dados saudáveis e emite um relatório técnico automatizado de Root Cause Analysis (RCA) — **tudo sem enviar nenhum dado confidencial para APIs na nuvem.**

## 🛠️ Tecnologias Utilizadas
* **Python 3.10+**
* **Polars:** Ingestão estrita e manipulação rápida de DataFrames.
* **Ollama:** Motor de inferência para LLMs locais (Privacy-First).
* **LLM (Llama 3.1 ou Qwen 2.5):** Raciocínio agêntico para triagem de logs de erro.

---

## 🚀 Como Executar o Projeto

Você pode rodar este projeto de duas maneiras: diretamente no seu computador ou na nuvem através do GitHub Codespaces (ideal caso esteja em uma rede corporativa com proxy restrito).

### Opção 1: Execução Local (Seu Computador)

**1. Instale o Ollama:**
Baixe e instale o motor local acessando [ollama.com](https://ollama.com).

**2. Baixe o modelo de IA:**
Abra o terminal e execute o comando abaixo para baixar o modelo (pode levar alguns minutos dependendo da sua conexão):
```bash
ollama pull llama3.1:8b
