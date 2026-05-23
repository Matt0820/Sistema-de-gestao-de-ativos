import sqlite3
from datetime import date


DB_PATH = "dados/databank.db"

# --- Helpers ---

def conexao_banco():
    conn = sqlite3.connect(DB_PATH) # Cria o arquivo se não existir
    conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
    return conn # Retorna a conexão para ser usada em outras funções


def row_para_dict(row): # Converte um resultado de consulta (sqlite3.Row) em um dicionário comum
    if row is None: # Se a consulta não retornou nada, retorna None
        return None # Caso contrário, converte a linha em um dicionário usando dict() e retorna
    return dict(row) # O dict() pode converter um sqlite3.Row em um dicionário onde as chaves são os nomes das colunas


def rows_para_lista_dict(rows): # Converte uma lista de resultados de consulta (lista de sqlite3.Row) em uma lista de dicionários comuns
    return [dict(r) for r in rows] # Usa uma list comprehension para iterar sobre cada linha (r) na lista de resultados (rows) e converte cada linha em um dicionário usando dict(r). Retorna a nova lista de dicionários.


# --- Criação de tabelas ---
def iniciar_banco():
    conectar_tabela_ativos()
    conectar_tabela_clientes()
    conectar_tabela_locacao()
    conectar_tabela_manutencao()


def conectar_tabela_ativos():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ativos (
            id_ativo INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            marca TEXT NOT NULL,
            ano INTEGER,
            placa TEXT UNIQUE,
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
    conexao = conexao_banco() # Abre a conexão com o banco de dados usando a função conexao_banco() definida anteriormente. Isso retorna um objeto de conexão que pode ser usado para executar comandos SQL.
    cursor = conexao.cursor() # Cria um cursor a partir da conexão. O cursor é usado para executar comandos SQL e recuperar resultados.

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            cnh TEXT NOT NULL UNIQUE
        )
    ''')

    conexao.commit() # Salva as alterações feitas no banco de dados (neste caso, a criação da tabela clientes). O commit é necessário para garantir que as mudanças sejam persistidas no arquivo do banco de dados.
    conexao.close() # Fecha a conexão com o banco de dados para liberar recursos.


def conectar_tabela_locacao():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locacao (
            id_locacao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_ativo INTEGER NOT NULL,
            data_ini DATE,
            duracao INTEGER,
            data_fim DATE,
            valor REAL,
            status TEXT,
            FOREIGN KEY (id_ativo) REFERENCES ativos(id_ativo),
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)   
        )
    ''')

    conexao.commit()
    conexao.close()

def conectar_tabela_manutencao():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manutencao (
            id_manutencao INTEGER PRIMARY KEY AUTOINCREMENT,
            id_ativo INTEGER NOT NULL,
            data DATE,
            data_fim DATE,
            descricao TEXT,
            custo REAL,
            FOREIGN KEY (id_ativo) REFERENCES ativos(id_ativo)
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

    cursor.execute('SELECT * FROM ativos WHERE id_ativo = ?', (id_ativo,))
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
        cursor.execute('SELECT * FROM ativos WHERE id_ativo = ?', (id_busca,))
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
    sql = f"UPDATE ativos SET {', '.join(campos)} WHERE id_ativo = ?"

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute(sql, tuple(valores))
    conexao.commit()
    conexao.close()


def apagar_ativo(id_ativo):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM ativos WHERE id_ativo = ?', (id_ativo,))

    conexao.commit()
    conexao.close()


def verificar_placa_existente(placa, id_ignorar=None):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    if id_ignorar:
        cursor.execute('SELECT * FROM ativos WHERE placa = ? AND id_ativo != ?', (placa, id_ignorar))
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

    cursor.execute('SELECT * FROM clientes WHERE id_cliente = ?', (id_cliente, ))
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
    sql = f"UPDATE clientes SET {', '.join(campos)} WHERE id_cliente = ?"

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute(sql, tuple(valores))
    conexao.commit()
    conexao.close()


def apagar_cliente(id_cliente):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM clientes WHERE id_cliente = ?', (id_cliente,))

    conexao.commit()
    conexao.close()


def verificar_cnh_existente(cnh):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM clientes WHERE cnh = ?', (cnh,))

    resultado = cursor.fetchone()
    conexao.close()
    return resultado is not None


# --- LOCAÇÕES ---
def cadastrar_locacao(id_cliente, id_ativo, data_ini, duracao, data_fim, valor, status='Ativa'):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO locacao (id_cliente, id_ativo, data_ini, duracao, data_fim, valor, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_cliente, id_ativo, data_ini, duracao, data_fim, valor, status))
    
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

    cursor.execute('SELECT * FROM locacao WHERE id_locacao = ?', (id_locacao,))
    resultado = cursor.fetchone()

    conexao.close()
    return row_para_dict(resultado)


def atualizar_locacao(id_locacao, dados: dict):
    if not dados:
        return
    allowed = ['id_cliente', 'id_ativo', 'data_ini', 'duracao', 'data_fim', 'valor', 'status']
    campos = []
    valores = []
    for k, v in dados.items():
        if k in allowed:
            campos.append(f"{k} = ?")
            valores.append(v)

    if not campos:
        return

    valores.append(id_locacao)
    sql = f"UPDATE locacao SET {', '.join(campos)} WHERE id_locacao = ?"

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute(sql, tuple(valores))
    conexao.commit()
    conexao.close()


def apagar_locacao(id_locacao):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM locacao WHERE id_locacao = ?', (id_locacao,))

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

    # atualiza status do ativo relacionado para "Disponível"
    ativo_ref = loc.get('id_ativo')
    if ativo_ref is not None:
        # tenta atualizar ativo por id ou placa
        ativo = buscar_ativo_por_id_ou_placa(ativo_ref)
        if ativo:
            atualizar_ativo(ativo.get('id_ativo'), {'status': 'Disponível'})

    return True

def inserir_manutencao(id_ativo, data, data_fim, descricao, custo):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('''
        INSERT INTO manutencao (id_ativo, data, data_fim, descricao, custo)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_ativo, data, data_fim, descricao, custo))

    conexao.commit()
    conexao.close()

def listar_manutencoes():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM manutencao')
    manutencoes = cursor.fetchall()

    conexao.close()
    return rows_para_lista_dict(manutencoes)

def buscar_manutencao_por_id(id_manutencao):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM manutencao WHERE id_manutencao = ?', (id_manutencao,))
    resultado = cursor.fetchone()

    conexao.close()
    return row_para_dict(resultado)

def atualizar_manutencao(id_manutencao, dados: dict):
    if not dados:
        return
    allowed = ['id_ativo', 'data', 'descricao', 'custo']
    campos = []
    valores = []
    for k, v in dados.items():
        if k in allowed:
            campos.append(f"{k} = ?")
            valores.append(v)

    if not campos:
        return

    valores.append(id_manutencao)
    sql = f"UPDATE manutencao SET {', '.join(campos)} WHERE id_manutencao = ?"

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute(sql, tuple(valores))
    conexao.commit()
    conexao.close()

def apagar_manutencao(id_manutencao):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute('DELETE FROM manutencao WHERE id_manutencao = ?', (id_manutencao,))

    conexao.commit()
    conexao.close()