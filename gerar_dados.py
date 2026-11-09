import pandas as pd
import random
from datetime import datetime, timedelta

# Configurações do dataset
NUM_ROWS = 5000
DIRTY_PERCENTAGE = 0.15  # 15% das linhas terão algum tipo de erro proposital

data = []
start_date = datetime.now()

for i in range(1, NUM_ROWS + 1):
    # 1. Geração da base limpa (Caminho Feliz)
    transaction_id = i
    date_obj = start_date - timedelta(days=random.randint(0, 30))
    date_str = date_obj.strftime("%Y-%m-%d") # Padrão ISO
    customer_id = random.randint(1000, 9999)
    product_value = round(random.uniform(50.0, 1500.0), 2)
    status = random.choice(["COMPLETED", "PENDING", "CANCELLED"])
    
    # 2. Injeção de sujeira (Anomalias)
    is_dirty = random.random() < DIRTY_PERCENTAGE
    
    if is_dirty:
        error_type = random.choice(["bad_date", "bad_value", "bad_customer"])
        
        if error_type == "bad_date":
            # Erro 1: Sistema de origem mandou a data no formato BR em vez de ISO
            date_str = date_obj.strftime("%d/%m/%Y")
            
        elif error_type == "bad_value":
            # Erro 2: Digitação errada, moeda misturada com número ou valor nulo
            product_value = random.choice(["N/A", "R$ 150,00", "NULL", ""])
            
        elif error_type == "bad_customer":
            # Erro 3: ID de cliente corrompido (String onde deveria ser Inteiro)
            customer_id = random.choice(["UNKNOWN", "Visitante", "---"])

    data.append([transaction_id, date_str, customer_id, product_value, status])

# 3. Exportação
df = pd.DataFrame(data, columns=["transaction_id", "date", "customer_id", "product_value", "status"])
file_name = "raw_transactions_data.csv"
df.to_csv(file_name, index=False)

print(f"✅ Arquivo '{file_name}' gerado com sucesso com {NUM_ROWS} linhas!")
print("\n🔍 Dê uma olhada na sujeira gerada (Amostra de 10 linhas):")
# Filtra apenas linhas que provavelmente contêm os erros injetados para exibir no console
dirty_sample = df[
    df['date'].str.contains('/') | 
    df['product_value'].astype(str).str.contains('[A-Z$]', regex=True) |
    df['customer_id'].astype(str).str.contains('[A-Z]', regex=True)
]
print(dirty_sample.head(10).to_string(index=False))