import sqlite3

def conectar_db():
    return sqlite3.connect("natacao.db")

def criar_base_dados():
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            metros INTEGER NOT NULL,
            minutos REAL NOT NULL,
            calorias INTEGER NOT NULL,
            estilo TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

def inserir_treino_db(data, metros, minutos, calorias, estilo):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO treinos (data, metros, minutos, calorias, estilo) VALUES (?, ?, ?, ?, ?)",
                   (data, metros, minutos, calorias, estilo))
    conexao.commit()
    conexao.close()

def eliminar_treino_db(treino_id):
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM treinos WHERE id = ?", (treino_id,))
    conexao.commit()
    conexao.close()

def buscar_todos_treinos_db():
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, data, metros, minutos, calorias, estilo FROM treinos ORDER BY data DESC")
    dados = cursor.fetchall()
    conexao.close()
    return dados

def buscar_treinos_grafico_db():
    conexao = conectar_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT data, metros, minutos FROM treinos ORDER BY data ASC LIMIT 10")
    dados = cursor.fetchall()
    conexao.close()
    return dados
