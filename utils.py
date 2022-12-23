from models import Pessoas, Atividades, Usuarios


#inseri dados na tabela pessoa
def insere_pessoas():
    pessoa = Pessoas(nome='Daniel', idade='45')
    print(pessoa)
    pessoa.save()

#consulta dados na tabela pessoa
def consulta_pessoas():
    pessoa = Pessoas.query.all()
    print(pessoa)
    #pessoa = Pessoas.query.filter_by(nome='maria').first()
    #print(pessoa.nome, pessoa.idade)

# altera dados na tabela pessoa
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Fernanda').first()

    pessoa.nome= 'maria'
    pessoa.save()
#exclui dados na tabela pessoa
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='maria').first()
    pessoa.delete()

def inseri_usuario(login,senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()


def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)
if __name__ == '__main__':
    #inseri_usuario("fernanda","123")
    #inseri_usuario("nogueira","432")
    consulta_todos_usuarios()
   #insere_pessoas()
    #consulta_pessoas()
   #altera_pessoa()
    #consulta_pessoas()
    #exclui_pessoa()