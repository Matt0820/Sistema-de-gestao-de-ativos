import sqlite3
import os

# Caminho do arquivo do banco de dados (na raiz do projeto)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'sistema.db')


def get_connection():
    """Retorna uma conexão com o banco de dados com row_factory configurada."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row       # permite acessar colunas pelo nome
    conn.execute("PRAGMA foreign_keys = ON")  # ativa integridade referencial
    return conn


def inicializar_banco():
    """Cria as tabelas se ainda não existirem."""
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de clientes (CNH é a chave primária natural)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            cnh    TEXT PRIMARY KEY,
            nome   TEXT NOT NULL,
            idade  INTEGER NOT NULL
        )
    ''')

    # Tabela de ativos (veículos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ativos (
            id_ativo         INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo           TEXT NOT NULL,
            marca            TEXT NOT NULL,
            ano              INTEGER NOT NULL,
            placa            TEXT NOT NULL UNIQUE,
            valor            REAL NOT NULL,
            diaria           REAL NOT NULL,
            data_aquisicao   TEXT NOT NULL,
            status           TEXT NOT NULL,
            depreciacao_final REAL NOT NULL
        )
    ''')

    # Tabela de locações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locacoes (
            id_locacao   INTEGER PRIMARY KEY AUTOINCREMENT,
            cnh_cliente  TEXT NOT NULL,
            id_ativo     INTEGER NOT NULL,
            data_inicio  TEXT NOT NULL,
            duracao      INTEGER NOT NULL,
            data_fim     TEXT NOT NULL,
            valor        REAL NOT NULL,
            status       TEXT NOT NULL,
            FOREIGN KEY (cnh_cliente) REFERENCES clientes(cnh),
            FOREIGN KEY (id_ativo)    REFERENCES ativos(id_ativo)
        )
    ''')

    conn.commit()
    conn.close()
    print("[DB] Banco de dados inicializado com sucesso.")
