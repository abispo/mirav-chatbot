import os
import psycopg2
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# Extrai filtros simples da query
def extract_filters(query: str):
    q = query.lower()

    filters = {
        "gender": None,
        "intensity": None,
        "best_time": None
    }

    if "masculino" in q:
        filters["gender"] = "Masculino"
    elif "feminino" in q:
        filters["gender"] = "Feminino"

    if "forte" in q:
        filters["intensity"] = "Forte"
    elif "leve" in q:
        filters["intensity"] = "Leve"

    if "noite" in q:
        filters["best_time"] = "Noite"
    elif "dia" in q:
        filters["best_time"] = "Dia"

    return filters


# Busca híbrida
def search_perfumes(query: str, limit=3):
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Embedding da pergunta
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = response.data[0].embedding

    # 2. Extrair filtros
    filters = extract_filters(query)

    # 3. Construir SQL dinâmico
    where_clauses = []
    params = []

    if filters["gender"]:
        where_clauses.append("p.gender = %s")
        params.append(filters["gender"])

    if filters["intensity"]:
        where_clauses.append("p.intensity = %s")
        params.append(filters["intensity"])

    if filters["best_time"]:
        where_clauses.append("p.best_time = %s")
        params.append(filters["best_time"])

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    # 4. Query principal
    sql = f"""
        SELECT pd.id, pd.content, p.name
        FROM perfume_documents pd
        JOIN perfumes p ON p.id = pd.perfume_id
        {where_sql}
        ORDER BY pd.embedding <-> %s::vector
        LIMIT %s
    """

    params.append(query_embedding)
    params.append(limit)

    cursor.execute(sql, params)
    results = cursor.fetchall()

    # Fallback (se não encontrou nada com filtro)
    if not results:
        cursor.execute("""
            SELECT pd.id, pd.content, p.name
            FROM perfume_documents pd
            JOIN perfumes p ON p.id = pd.perfume_id
            ORDER BY pd.embedding <-> %s::vector
            LIMIT %s
        """, (query_embedding, limit))

        results = cursor.fetchall()

    cursor.close()

    return results


# Teste no terminal
if __name__ == "__main__":
    while True:
        query = input("\nDigite a pergunta: ")

        results = search_perfumes(query)

        print("\n🔎 Resultados:\n")

        for r in results:
            print(f"Perfume: {r[2]}")
            print(f"Resumo: {r[1][:200]}...")
            print("-" * 50)