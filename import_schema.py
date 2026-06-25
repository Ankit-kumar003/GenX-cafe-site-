from app import app
from models.db import query

def run_schema():
    print("\n=== STARTING SCHEMA IMPORT ===")
    
    # 1. schema.sql file ko read karna
    try:
        with open('schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
    except FileNotFoundError:
        print("Error: 'schema.sql' file nahi mili! Check karein ki aap sahi folder me hain.")
        return

    # Semicolon se saari queries ko alag alag karna
    queries = sql_script.split(';')

    # 2. Flask Application Context me execute karna
    with app.app_context():
        for q in queries:
            clean_query = q.strip()
            if clean_query:
                try:
                    # Sirf un queries ko chalayein jo comments nahi hain
                    if not clean_query.startswith('--') and not clean_query.startswith('/*'):
                        query(clean_query, commit=True)
                except Exception as e:
                    # Agar table pehle se bani ho toh ye error ignore hoga
                    print(f"Notice (Ignored if already exists): {e}")

    print("\n=== SCHEMA IMPORTED SUCCESSFULLY! ===")

if __name__ == '__main__':
    run_schema()