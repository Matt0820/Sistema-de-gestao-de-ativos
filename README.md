# SISTEMA DE LOCAÇÃO DE VEÍCULOS 

##  Descrição do Sistema
Sistema desenvolvido em **Python** com o objetivo de facilitar o controle e a organização de uma locadora de veículos.

O sistema permite gerenciar **clientes, veículos (ativos) e locações**, garantindo mais controle e rastreabilidade das operações.

Com ele é possível:
- Controlar disponibilidade de veículos
- Gerenciar locações ativas e finalizadas
- Consultar e atualizar dados rapidamente

---

## Funcionalidades Implementadas

### Gestão de Clientes
- Cadastro de clientes
- Edição de dados
- Exclusão de clientes
- Listagem completa
- Busca por critérios (CNH,Placa e ID)
- Validação de maioridade
- Bloqueio de edição e exclusão, quando há locação ativa

---

### Gestão de Ativos (Veículos)
- Cadastro de ativos
- Edição de dados
- Exclusão de ativos
- Listagem de ativos
- Consulta de disponibilidade
- Controle de status:
  - `Disponível`
  - `Alugado`
- Bloqueio de edição e exclusão, quando o veículo está alugado

---

### Gestão de Locações
- Criação de locações
- Finalização de locações
- Listagem de locações
- Controle de status:
  - `Ativa`
  - `Finalizada`
- Definição de data de início e duração da locação
- Validação para impedir:
  - Cliente com múltiplas locações ativas
  - Veículo já alugado

---

### Busca e Filtros
- Busca flexível de clientes e veículos
- Filtros dinâmicos sem depender de ID único
- Facilita consultas rápidas no sistema

---

### Relatórios
- Listagem de ativos disponíveis
- Visualização de locações ativas
- Organização geral dos dados cadastrados

---

## Estrutura de Dados

### 1. Cliente
- **CNH** — `String` -> Carteira Nacional de Habilitação
- **Nome** — `String` -> Nome do cliente
- **Idade** — `Int` -> Idade do cliente

---

### 2. Ativo (Veículo)
- **Modelo** — `String` -> Modelo do veículo
- **Marca** — `String` -> Marca do veículo
- **Placa** — `String` -> número de identificação
- **Status** — `String` -> Disponibilidade do ativo
  - `Disponível`
  - `Alugado`

---

### 3. Locação
- **Cliente** — `Cliente` -> Nome do cliente
- **Ativo** — `Ativo` -> Indica o modelo e marca do ativo
- **Data_Inicio** — `Date` -> Data do inicio da locação
- **Duração** — `Int` -> Duração em Dias
- **Data_Fim** — `Date` -> Data final da locação
- **Status** — `String` -> Status atual da locação
  - `Ativa`
  - `Finalizada`

---

## Arquitetura do Projeto


Estrutura do nosso projeto: 

``` 
    cadastroecontroledeativos/
    ├── controle/
    │   ├─ ativo_controle.py # metodos de controle de ativo
    |   ├─ cliente_controle.py # metodos de controle do cliente
    |   └── locacao_controle.py # metodos de controle de locação 
    ├── modelos/
    |   ├─ ativo.py # Classe ativo
    |   ├─ cliente.py # Classe Cliente
    │   └─ locacao.py # Classe Locação
    ├── main.py # Interface e ligação central do sistema
    └── README.md
```


---

## Problema Resolvido

Problemas enfrentados por pequenas locadoras:
- Falta de organização
- Dificuldade em rastrear veículos
- Erros em locações
- Perda de informações

Este sistema resolve esses pontos ao centralizar e padronizar o controle.

---

## Possíveis Melhorias Futuras

### Persistência de Dados
- Implementar banco de dados
- Salvar dados em arquivos (`JSON`,`CSV` ou `TXT`) para manter informações entre execuções
- Evitar perda de dados ao encerrar o sistema

---

### Regras de Negócio Mais Avançadas
- Controle de multas por atraso na devolução
- Histórico completo de locações por cliente

---

### Relatórios Avançados
- Relatório de faturamento
- Veículos mais alugados
- Clientes mais ativos
- Exportar relatórios (PDF/CSV/TXT)

---

### Segurança e Validação
- Melhorar a validação de CNH
- Sistema de autenticação (login/senha) para os operadores do sistema
- Controle de permissões (admin/operador) para os operadores do sistema

---

## Como Executar

1. Certifique-se de ter o Python 3.14 instalado
2. Baixe o projeto  
3. Acesse a pasta no Terminal
```bash
cd sistema-de-gestao-de-ativos
```
4. Execute o arquivo main.py

```bash
python main.py
```
## Autores
1. Giovanni Bruno Giovanelli
2. Lucas Gabriel Genovezi
3. Mateus Henrique Oliveira Vieira
4. Thiago Henrique Bonierski
5. Vitor Gabriel Gonçalves