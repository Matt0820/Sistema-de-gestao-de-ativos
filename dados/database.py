import os
import sqlite3
from datetime import date

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "databank.db")


# --- Helpers ---

def conexao_banco():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


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
    conectar_tabela_manutencao()
    atualizar_categorias_manutencao()


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
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            cnh TEXT NOT NULL UNIQUE
        )
    ''')
    conexao.commit()
    conexao.close()


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
            status TEXT DEFAULT 'Ativa',
            id_ativo INTEGER NOT NULL,
            categoria TEXT,
            data DATE,
            data_fim DATE,
            descricao TEXT,
            custo REAL,
            FOREIGN KEY (id_ativo) REFERENCES ativos(id_ativo)
        )
    ''')
    cursor.execute("PRAGMA table_info(manutencao)")
    existing_columns = [row['name'] for row in cursor.fetchall()]
    if 'categoria' not in existing_columns:
        cursor.execute('ALTER TABLE manutencao ADD COLUMN categoria TEXT')
    conexao.commit()
    conexao.close()


def classificar_categoria_manutencao(descricao):
    if not descricao:
        return 'Outros'

    texto = descricao.lower()
    if any(token in texto for token in [
        'óleo', 'oleo', 'troca de óleo', 'troca de oleo', 'filtro', 'motor',
        'embreagem', 'freio', 'freios', 'pneu', 'suspensão', 'suspensao',
        'amortecedor', 'câmbio', 'cambio'
    ]):
        return 'Mecânica'

    if any(token in texto for token in [
        'fiação', 'fiacao', 'elétrico', 'eletrico', 'bateria', 'lampada',
        'lâmpada', 'farol', 'painel', 'alarme', 'radio', 'rádio',
        'ar condicionado', 'ar-condicionado', 'sensor', 'painel', 'luz'
    ]):
        return 'Elétrica'

    if any(token in texto for token in [
        'pintura', 'polimento', 'estética', 'estetica', 'limpeza',
        'higienização', 'higienizacao', 'estofado', 'adesivo', 'lataria'
    ]):
        return 'Estética'

    return 'Outros'


def atualizar_categorias_manutencao():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT id_manutencao, descricao, categoria FROM manutencao")
    manutencoes = cursor.fetchall()

    for manutencao in manutencoes:
        categoria_atual = manutencao['categoria']
        descricao = manutencao['descricao']
        if categoria_atual is None or str(categoria_atual).strip() == '':
            categoria = classificar_categoria_manutencao(descricao)
            cursor.execute(
                'UPDATE manutencao SET categoria = ? WHERE id_manutencao = ?',
                (categoria, manutencao['id_manutencao'])
            )

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
    """Busca ativo por ID (inteiro) ou por placa (string)."""
    conexao = conexao_banco()
    cursor = conexao.cursor()

    try:
        id_busca = int(busca)
        cursor.execute('SELECT * FROM ativos WHERE id_ativo = ?', (id_busca,))
        resultado = cursor.fetchone()
        if resultado:
            conexao.close()
            return row_para_dict(resultado)
    except (ValueError, TypeError):
        pass

    cursor.execute('SELECT * FROM ativos WHERE placa = ?', (str(busca).upper(),))
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
        cursor.execute('SELECT 1 FROM ativos WHERE placa = ? AND id_ativo != ?', (placa, id_ignorar))
    else:
        cursor.execute('SELECT 1 FROM ativos WHERE placa = ?', (placa,))
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
    cursor.execute('SELECT * FROM clientes WHERE id_cliente = ?', (id_cliente,))
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

def buscar_cliente_por_id_ou_cnh(busca):
    conexao = conexao_banco()
    cursor = conexao.cursor()
    try:
        id_busca = int(busca)
        cursor.execute('SELECT * FROM clientes WHERE id_cliente = ?', (id_busca,))
        resultado = cursor.fetchone()
        if resultado:
            conexao.close()
            return row_para_dict(resultado)
    except (ValueError, TypeError):
        pass

    cursor.execute('SELECT * FROM clientes WHERE cnh = ?', (str(busca).upper(),))
    resultado = cursor.fetchone()
    conexao.close()
    return row_para_dict(resultado)

def apagar_cliente(id_cliente=None, cnh=None):
    conexao = conexao_banco()
    cursor = conexao.cursor()
    if id_cliente is not None:
        cursor.execute('DELETE FROM clientes WHERE id_cliente = ?', (id_cliente,))
    elif cnh is not None:
        cursor.execute('DELETE FROM clientes WHERE cnh = ?', (cnh,))
    else:
        conexao.close()
        return

    conexao.commit()
    conexao.close()


def verificar_cnh_existente(cnh):
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT 1 FROM clientes WHERE cnh = ?', (cnh,))
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


def listar_locacoes_completas():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute('''
        SELECT
            locacao.id_locacao,
            locacao.id_cliente,
            locacao.id_ativo,
            clientes.nome AS cliente,
            ativos.modelo AS ativo,
            ativos.placa,
            locacao.data_ini,
            locacao.duracao,
            locacao.data_fim,
            locacao.valor,
            locacao.status
        FROM locacao
        JOIN clientes ON locacao.id_cliente = clientes.id_cliente
        JOIN ativos ON locacao.id_ativo = ativos.id_ativo
    ''')
    resultado = cursor.fetchall()
    conexao.close()
    return rows_para_lista_dict(resultado)


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
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM locacao WHERE status = 'Ativa'")
    locacoes = cursor.fetchall()
    conexao.close()
    return rows_para_lista_dict(locacoes)


def listar_locacoes_finalizadas():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM locacao WHERE status = 'Finalizada'")
    locacoes = cursor.fetchall()
    conexao.close()
    return rows_para_lista_dict(locacoes)


def finalizar_locacao(id_locacao):
    loc = buscar_locacao_por_id(id_locacao)
    if loc is None:
        return False

    data_fim = date.today()
    atualizar_locacao(id_locacao, {'status': 'Finalizada', 'data_fim': data_fim})

    id_ativo = loc.get('id_ativo')
    if id_ativo is not None:
        atualizar_ativo(id_ativo, {'status': 'Disponível'})

    return True


# --- MANUTENÇÃO ---

def inserir_manutencao(id_ativo, categoria, data, data_fim, descricao, custo):
    if not categoria or not str(categoria).strip():
        categoria = classificar_categoria_manutencao(descricao)

    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO manutencao (id_ativo, categoria, data, data_fim, descricao, custo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_ativo, categoria, data, data_fim, descricao, custo))
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
    allowed = ['id_ativo', 'data', 'data_fim', 'categoria', 'descricao', 'custo']
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

def listar_manutencoes_ativas():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM manutencao WHERE status = 'Ativa'")
    resultado = cursor.fetchall()
    conexao.close()
    return rows_para_lista_dict(resultado)


def listar_manutencoes_finalizadas():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM manutencao WHERE status = 'Finalizada'")
    resultado = cursor.fetchall()
    conexao.close()
    return rows_para_lista_dict(resultado)


def finalizar_manutencao(id_manutencao):
    manutencao = buscar_manutencao_por_id(id_manutencao)
    if manutencao is None:
        return False
    atualizar_manutencao(id_manutencao, {'status': 'Finalizada'})
    atualizar_ativo(manutencao['id_ativo'], {'status': 'Disponível'})
    return True


#Relatorio financeiro

def relatorio_financeiro_mes(ano, mes):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    # Entradas: locações iniciadas no mês
    cursor.execute("""
        SELECT COALESCE(SUM(valor), 0) as total
        FROM locacao
        WHERE strftime('%Y', data_ini) = ?
          AND strftime('%m', data_ini) = ?
    """, (str(ano), f"{mes:02d}"))
    entradas = cursor.fetchone()['total']

    # Saídas: manutenções iniciadas no mês
    cursor.execute("""
        SELECT COALESCE(SUM(custo), 0) as total
        FROM manutencao
        WHERE strftime('%Y', data) = ?
          AND strftime('%m', data) = ?
    """, (str(ano), f"{mes:02d}"))
    saidas = cursor.fetchone()['total']

    # Detalhes das locações do mês
    cursor.execute("""
        SELECT locacao.id_locacao, clientes.nome AS cliente,
               ativos.modelo AS ativo, ativos.placa,
               locacao.data_ini, locacao.data_fim,
               locacao.valor, locacao.status
        FROM locacao
        JOIN clientes ON locacao.id_cliente = clientes.id_cliente
        JOIN ativos   ON locacao.id_ativo   = ativos.id_ativo
        WHERE strftime('%Y', locacao.data_ini) = ?
          AND strftime('%m', locacao.data_ini) = ?
        ORDER BY locacao.data_ini
    """, (str(ano), f"{mes:02d}"))
    locacoes_mes = rows_para_lista_dict(cursor.fetchall())

    # Detalhes das manutenções do mês
    cursor.execute("""
        SELECT manutencao.id_manutencao, ativos.modelo AS ativo,
               ativos.placa, manutencao.data, manutencao.descricao,
                             manutencao.custo, manutencao.categoria, manutencao.status
        FROM manutencao
        JOIN ativos ON manutencao.id_ativo = ativos.id_ativo
        WHERE strftime('%Y', manutencao.data) = ?
          AND strftime('%m', manutencao.data) = ?
        ORDER BY manutencao.data
    """, (str(ano), f"{mes:02d}"))
    manutencoes_mes = rows_para_lista_dict(cursor.fetchall())

    conexao.close()

    return {
        'entradas': entradas,
        'saidas': saidas,
        'liquido': entradas - saidas,
        'locacoes': locacoes_mes,
        'manutencoes': manutencoes_mes,
    }
    
def relatorio_financeiro_ano(ano):
    conexao = conexao_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(valor), 0) as total
        FROM locacao
        WHERE strftime('%Y', data_ini) = ?
    """, (str(ano),))
    entradas = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COALESCE(SUM(custo), 0) as total
        FROM manutencao
        WHERE strftime('%Y', data) = ?
    """, (str(ano),))
    saidas = cursor.fetchone()['total']

    cursor.execute("""
        SELECT locacao.id_locacao, clientes.nome AS cliente,
               ativos.modelo AS ativo, ativos.placa,
               locacao.data_ini, locacao.data_fim,
               locacao.valor, locacao.status,
               strftime('%m', locacao.data_ini) AS mes
        FROM locacao
        JOIN clientes ON locacao.id_cliente = clientes.id_cliente
        JOIN ativos   ON locacao.id_ativo   = ativos.id_ativo
        WHERE strftime('%Y', locacao.data_ini) = ?
        ORDER BY locacao.data_ini
    """, (str(ano),))
    locacoes_ano = rows_para_lista_dict(cursor.fetchall())

    cursor.execute("""
        SELECT manutencao.id_manutencao, ativos.modelo AS ativo,
               ativos.placa, manutencao.data, manutencao.descricao,
               manutencao.custo, manutencao.categoria, manutencao.status,
               strftime('%m', manutencao.data) AS mes
        FROM manutencao
        JOIN ativos ON manutencao.id_ativo = ativos.id_ativo
        WHERE strftime('%Y', manutencao.data) = ?
        ORDER BY manutencao.data
    """, (str(ano),))
    manutencoes_ano = rows_para_lista_dict(cursor.fetchall())

    conexao.close()

    return {
        'entradas': entradas,
        'saidas': saidas,
        'liquido': entradas - saidas,
        'locacoes': locacoes_ano,
        'manutencoes': manutencoes_ano,
    }