#Importa as libs necessarias
import sqlite3
#importa a lib datetime
from datetime import date

#deixa um caminho para o banco de dados
DB_PATH = "databank.db"

#cria a conexao com o banco de dados
def conexao_banco():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

#transforma uma linha em um dicionario
def row_para_dict(row):
    if row is None:
        return None
    return dict(row)


def rows_para_lista_dict(rows):
    return [dict(r) for r in rows]


# --- Criação de tabelas ---
def iniciar_banco():
    conectar_tabela_ativos()
    conectar_tabela_clientes()
    conectar_tabela_locacao()


def conectar_tabela_ativos():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ativos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            marca TEXT,
            ano INTEGER,
            placa TEXT,
            valor REAL,
            diaria REAL,
            data DATE,
            status TEXT,
            depreciacao REAL
        )
    ''')

    conexao.commit()
    conexao.close()


def conectar_tabela_clientes():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_transacao_mensal INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            cnh TEXT NOT NULL
        )
    ''')

    conexao.commit()
    conexao.close()


def conectar_tabela_locacao():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locacao (
            id_transacao_mensal INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_obj TEXT NOT NULL,
            ativo_obj TEXT NOT NULL,
            data_ini DATE,
            duracao TEXT,
            data_fim DATE,
            valor REAL,
            status TEXT
        )
    ''')

    conexao.commit()
    conexao.close()


# --- ATIVOS ---
def cadastrar_ativo(modelo, marca, ano, placa, valor, diaria, data, status="Disponível", depreciacao=None):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO ativos (modelo, marca, ano, placa, valor, diaria, data, status, depreciacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (modelo, marca, ano, placa, valor, diaria, data, status, depreciacao))

    conexao.commit()
    conexao.close()


def listar_ativos():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM ativos')
    ativos = cursor.fetchall()

    conexao.close()
    return rows_para_lista_dict(ativos)


def buscar_ativo_por_id(id_ativo):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM ativos WHERE id = ?', (id_ativo,))
    resultado = cursor.fetchone()

    conexao.close()
    return row_para_dict(resultado)


def buscar_ativo_por_placa(placa):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM ativos WHERE placa = ?', (placa,))
    resultado = cursor.fetchone()

    conexao.close()
    return row_para_dict(resultado)


def buscar_ativo_por_id_ou_placa(busca):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    # tenta por id (int) primeiro
    try:
        id_busca = int(busca)
    except Exception:
        id_busca = None

    if id_busca is not None:
        cursor.execute('SELECT * FROM ativos WHERE id = ?', (id_busca,))
        resultado = cursor.fetchone()
        if resultado:
            conexao.close()
            return row_para_dict(resultado)

    # busca por placa (string)
    cursor.execute('SELECT * FROM ativos WHERE placa = ?', (busca,))
    resultado = cursor.fetchone()

    conexao.close()
    return row_para_dict(resultado)


def atualizar_ativo(id_ativo, dados: dict):
    if not dados:
        return
    allowed = ['modelo', 'marca', 'ano', 'placa', 'valor', 'diaria', 'data', 'status', 'depreciacao']
    campos = []
    valores = []
    for k, v in dados.items():
        if k in allowed:
            campos.append(f"{k} = ?")
            valores.append(v)

    if not campos:
        return

    valores.append(id_ativo)
    sql = f"UPDATE ativos SET {', '.join(campos)} WHERE id = ?"

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute(sql, tuple(valores))
    conexao.commit()
    conexao.close()


def apagar_ativo(id_ativo):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM ativos WHERE id = ?', (id_ativo,))

    conexao.commit()
    conexao.close()


def verificar_placa_existente(placa, id_ignorar=None):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    if id_ignorar:
        cursor.execute('SELECT * FROM ativos WHERE placa = ? AND id != ?', (placa, id_ignorar))
    else:
        cursor.execute('SELECT * FROM ativos WHERE placa = ?', (placa,))

    resultado = cursor.fetchone()
    conexao.close()
    return resultado is not None


# --- CLIENTES ---
def cadastrar_cliente(nome, idade, cnh):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO clientes (nome, idade, cnh)
        VALUES (?, ?, ?)
    ''', (nome, idade, cnh))

    conexao.commit()
    conexao.close()


def listar_clientes():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()

    conexao.close()
    return rows_para_lista_dict(clientes)


def buscar_cliente_por_id(id_cliente):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM clientes WHERE id_transacao_mensal = ?', (id_cliente,))
    resultado = cursor.fetchone()

    conexao.close()
    return row_para_dict(resultado)


def buscar_cliente_por_cnh(cnh):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM clientes WHERE cnh = ?', (cnh,))
    resultado = cursor.fetchone()

    conexao.close()
    return row_para_dict(resultado)


def atualizar_cliente(id_cliente, dados: dict):
    if not dados:
        return
    allowed = ['nome', 'idade', 'cnh']
    campos = []
    valores = []
    for k, v in dados.items():
        if k in allowed:
            campos.append(f"{k} = ?")
            valores.append(v)

    if not campos:
        return

    valores.append(id_cliente)
    sql = f"UPDATE clientes SET {', '.join(campos)} WHERE id_transacao_mensal = ?"

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute(sql, tuple(valores))
    conexao.commit()
    conexao.close()


def apagar_cliente(id_cliente):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM clientes WHERE id_transacao_mensal = ?', (id_cliente,))

    conexao.commit()
    conexao.close()


def verificar_cnh_existente(cnh, id_ignorar=None):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    if id_ignorar:
        cursor.execute('SELECT * FROM clientes WHERE cnh = ? AND id_transacao_mensal != ?', (cnh, id_ignorar))
    else:
        cursor.execute('SELECT * FROM clientes WHERE cnh = ?', (cnh,))

    resultado = cursor.fetchone()
    conexao.close()
    return resultado is not None


# --- LOCAÇÕES ---
def cadastrar_locacao(cliente_obj, ativo_obj, data_ini, duracao, data_fim, valor, status='Ativa'):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO locacao (cliente_obj, ativo_obj, data_ini, duracao, data_fim, valor, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (cliente_obj, ativo_obj, data_ini, duracao, data_fim, valor, status))

    conexao.commit()
    conexao.close()


def listar_locacoes():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM locacao')
    locacoes = cursor.fetchall()

    conexao.close()
    return rows_para_lista_dict(locacoes)


def buscar_locacao_por_id(id_locacao):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM locacao WHERE id_transacao_mensal = ?', (id_locacao,))
    resultado = cursor.fetchone()

    conexao.close()
    return row_para_dict(resultado)


def atualizar_locacao(id_locacao, dados: dict):
    if not dados:
        return
    allowed = ['cliente_obj', 'ativo_obj', 'data_ini', 'duracao', 'data_fim', 'valor', 'status']
    campos = []
    valores = []
    for k, v in dados.items():
        if k in allowed:
            campos.append(f"{k} = ?")
            valores.append(v)

    if not campos:
        return

    valores.append(id_locacao)
    sql = f"UPDATE locacao SET {', '.join(campos)} WHERE id_transacao_mensal = ?"

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute(sql, tuple(valores))
    conexao.commit()
    conexao.close()


def apagar_locacao(id_locacao):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM locacao WHERE id_transacao_mensal = ?', (id_locacao,))

    conexao.commit()
    conexao.close()


def listar_locacoes_ativas():
    todas = listar_locacoes()
    def norm(s):
        return (s or '').strip().lower()
    return [l for l in todas if norm(l.get('status')) in ('ativa', 'ativo', 'em andamento', 'alugada')]


def listar_locacoes_finalizadas():
    todas = listar_locacoes()
    def norm(s):
        return (s or '').strip().lower()
    return [l for l in todas if norm(l.get('status')) in ('finalizada', 'encerrada', 'finalizado')]


def finalizar_locacao(id_locacao, data_fim=None):
    loc = buscar_locacao_por_id(id_locacao)
    if loc is None:
        return False

    if data_fim is None:
        data_fim = date.today()

    atualizar_locacao(id_locacao, {'status': 'Finalizada', 'data_fim': data_fim})

    # atualiza status do ativo relacionado (ativo_obj pode ser placa ou id)
    ativo_ref = loc.get('ativo_obj')
    if ativo_ref is not None:
        # tenta atualizar ativo por id ou placa
        ativo = buscar_ativo_por_id_ou_placa(ativo_ref)
        if ativo:
            atualizar_ativo(ativo.get('id'), {'status': 'Disponível'})

    return True
