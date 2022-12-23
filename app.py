from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades
import json

app = Flask(__name__)
api = Api(app)

class Pessoa(Resource):

#pega os dados
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome =nome).first()

        try:
            response = {
            'nome': pessoa.nome,
            'idade': pessoa.idade,
            'id': pessoa.id
            }

        except AttributeError:
            response={
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }
        return response
#altera os dados

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados :
            pessoa.nome= dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()

        response ={
            'id': pessoa.id,
            'nome':pessoa.nome,
            'idade': pessoa.idade

        }
        return response
    def delete(self,nome):
        pessoa = Pessoas.query.filter_by(nome= nome).first()
        mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.nome)
        pessoa.delete()
        return {'status': 'sucesso',
                'mensagem': mensagem
                }




class Pessoas_All(Resource):

    def get(self):
        pessoas= Pessoas.query.all()
        response =[{'id':i.id, 'nome':i.nome,'idade':i.idade} for i in pessoas]


        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'],idade = dados['idade'])
        pessoa.save()
        response ={ 'nome': pessoa.nome,
                    'idade': pessoa.idade,
                    'id': pessoa.id


        }
        return response


class AtividadesSelecionada(Resource):

    def get(self,nome):
        pessoa_select = Pessoas.query.filter_by(nome=nome).first()
        atividades = Atividades.query.filter_by(pessoa_id=pessoa_select.id)
        mensagem = 'Pessoa {} esta pessoa encontraada'.format(pessoa_select.id)
        response =[{"nome": i.nome, "status":i.status, "pessoa_id": i.pessoa_id, "id":i.id } for i in atividades]



        return  response





class AtividadesTrocarStatus(Resource):


    def get(self,id):

        atividades= Atividades.query.filter_by(id=id).first()
        try:

            response = [{"nome": atividades.nome, "status": atividades.status, "pessoa_id": atividades.pessoa_id}]
        except AttributeError:
            response= {"status": "error",
                       "mensagem": "id nao encontrado"}

        return response

    def put(self,id):
        atividades = Atividades.query.filter_by(id=id).first()
        if atividades.status=='pendente':

            atividades.status='concluido'
            atividades.save()
        mensagem = 'Atividade  teve o status alterado para {} '.format(atividades.status)

        return mensagem

    def delete(self,id):
        atividades= Atividades.query.filter_by(id=id).first()


        try:
            mensagem = 'Atividade com id {} excluida com sucesso'.format(atividades.id)
            atividades.delete()
        except AttributeError:
            mensagem = "id não encontrado"

        return {
            "status": mensagem
        }


        




class ListaAtividades(Resource):

    def get(self):
        atividades = Atividades.query.all()
        response = []
        for i in atividades:
            dado = Pessoas.query.filter_by(id= i.id).first()

            print(dado)
            if dado != None:
                nome= dado.nome
            else:
                nome = 'não informado'

            response.append({'nome': i.nome,
                'status': i.status,
                'pessoa_id': nome,
                'id': i.id

            })
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome= dados['nome'],status= dados['status'],pessoa= pessoa)
        atividade.save()
        response ={
            'pessoa': atividade.pessoa.id,
            'nome': atividade.nome,
            'status': atividade.status,
            'id':atividade.id
        }
        return response




api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(Pessoas_All, '/pessoa/')
api.add_resource(ListaAtividades, '/atividade/')
api.add_resource(AtividadesSelecionada, '/atividade/<string:nome>/')
api.add_resource(AtividadesTrocarStatus,'/atividade/<int:id>/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
