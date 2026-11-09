import polars as pl
import json
import urllib.request
import urllib.error

# 1. Definimos o esquema esperado (O Contrato de Dados)
ESQUEMA_ESPERADO = {
    "transaction_id": pl.Int64,
    "date": pl.Date,
    "customer_id": pl.Int64,
    "product_value": pl.Float64,
    "status": pl.Utf8
}

ARQUIVO_ENTRADA = "raw_transactions_data.csv"
MODELO_LLM = "llama3.1:8b" 

# Função para chamar o Ollama contornando o Proxy via urllib
def chamar_ollama_local(prompt):
    url = "http://127.0.0.1:11434/api/chat"
    data = json.dumps({
        "model": MODELO_LLM,
        "messages": [
            {"role": "system", "content": "Você é um engenheiro de dados sênior. Responda em português, usando formato Markdown estruturado, de forma direta e técnica."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }).encode("utf-8")
    
    # Cria um handler de proxy vazio para forçar conexão direta no localhost
    proxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_handler)
    
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with opener.open(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["message"]["content"]
    except urllib.error.URLError as e:
        return f"Erro ao conectar com Ollama: {e}"

def executar_pipeline():
    print("🚀 [PIPELINE] Iniciando ingestão de dados em modo estrito...")
    try:
        df = pl.read_csv(ARQUIVO_ENTRADA, schema=ESQUEMA_ESPERADO)
        print("✅ [PIPELINE] Ingestão concluída com sucesso! Nenhum erro.")
        
    except pl.exceptions.ComputeError as e:
        mensagem_erro = str(e)
        print(f"❌ [PIPELINE] Falha crítica detectada na tipagem: {mensagem_erro.splitlines()[0]}")
        print("🚨 [SISTEMA] Acionando Agente de Auto-Cura (DataOps)...")
        agente_auto_cura(mensagem_erro)

def agente_auto_cura(erro_polars):
    print("🤖 [AGENTE] Analisando o lote corrompido. Lendo dados em modo de segurança (String)...")
    
    df_raw = pl.read_csv(ARQUIVO_ENTRADA, schema_overrides={"date": pl.Utf8, "customer_id": pl.Utf8, "product_value": pl.Utf8})
    
    df_casted = df_raw.with_columns([
        pl.col("date").str.to_date("%Y-%m-%d", strict=False),
        pl.col("customer_id").cast(pl.Int64, strict=False),
        pl.col("product_value").cast(pl.Float64, strict=False)
    ])
    
    mascara_erros = df_casted["date"].is_null() | df_casted["customer_id"].is_null() | df_casted["product_value"].is_null()
    
    df_saudavel = df_casted.filter(~mascara_erros)
    df_quarentena = df_raw.filter(mascara_erros) 
    
    print(f"🩹 [AGENTE] Triagem feita: {len(df_saudavel)} linhas salvas. {len(df_quarentena)} linhas enviadas para a quarentena.")
    
    amostra_sujeira = df_quarentena.head(5).to_dicts()
    
    prompt = f"""
    Você é um Engenheiro de DataOps Autônomo. 
    A pipeline de ingestão falhou ao tentar ler um arquivo CSV.
    
    Erro do Polars: {erro_polars}
    
    Amostra das linhas que causaram o erro (dados brutos):
    {json.dumps(amostra_sujeira, indent=2)}
    
    Sua tarefa:
    1. Diagnostique o problema (Ex: Qual coluna está com formato errado? O que está escrito lá?).
    2. Escreva um 'Root Cause Analysis' (RCA) muito breve.
    3. Confirme que os dados corrompidos foram isolados para análise manual e o lote principal seguiu para o Data Warehouse.
    """
    
    print("🧠 [AGENTE] Escrevendo relatório de incidente (Inferência LLM Local)...")
    
    relatorio = chamar_ollama_local(prompt)
    
    df_saudavel.write_parquet("dados_limpos.parquet")
    df_quarentena.write_csv("dados_quarentena.csv")
    
    with open("relatorio_incidente.md", "w", encoding="utf-8") as f:
        f.write(relatorio)
        
    print("\n================ RELATÓRIO DO AGENTE ================\n")
    print(relatorio)
    print("\n=====================================================")
    print("📁 [SISTEMA] Arquivos gerados:")
    print("  - dados_limpos.parquet (Pronto para o Data Warehouse)")
    print("  - dados_quarentena.csv (Para análise do time de negócios)")
    print("  - relatorio_incidente.md (Log do agente)")

if __name__ == "__main__":
    executar_pipeline()