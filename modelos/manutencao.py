from modelos.ativo import Ativo

class Manutencao:

#metodo construtor da classe manutencao (ps: pretendo revisar isso depois, pois preciso revisar as variaveis que existem na manutenção)
    def __init__(self,data_realizacao,preivisao_retorno,id_manutencao,valor,categoria):
        self.ativo_obj = Ativo() 
        self.data_realizacao = data_realizacao
        self.preivisao_retorno = preivisao_retorno
        self.id_manutencao = id_manutencao
        self.status = "Finalizado"
        self.valor = valor
#metodo para exibir dados da manutenção (ps: nao sei as variaveis ainda)
    def exibirDados(self):
        print( "="*5 + "Dados da Manutencao" + "="*5)
        print(f"ID da Manutencao: {self.id_manutencao}")
        print(f"Ativo: {self.ativo_obj.marca + self.ativo_obj.modelo + self.ativo_obj.placa}")
        print(f"Valor: {self.valor}")
        print(f"Previsao de Retorno: {self.preivisao_retorno}")
        print(f"Status: {self.status}")