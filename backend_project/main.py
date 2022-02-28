from datetime import datetime

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import pika
from json import dumps


db_connect = create_engine('sqlite:///db_scholl_app.sqlite')
app = Flask(__name__)
api = Api(app)


class OperatorDb():
    def getAlunoById(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from Alunos where AlunosId =%d" % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        return result

    def getPaisByUsername(username):
        conn = db_connect.connect()
        query = conn.execute("select * from Pais")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        for i in result:
            if username == i['Username']:
                return i
        pass

    def getPaisByName(name):
        conn = db_connect.connect()
        query = conn.execute("select * from Pais")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        for i in result:
            if name == i['Nome']:
                return i
        pass

    def getProfessorByUsername(username):
        conn = db_connect.connect()
        query = conn.execute("select * from Professores")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        for i in result:
            if username == i['Username']:
                return i
        pass

    def getProfessorByName(name):
        conn = db_connect.connect()
        query = conn.execute("select * from Professores")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        for i in result:
            if name == i['Nome']:
                return i
        pass

    def getAlunoByUsername(username):
        conn = db_connect.connect()
        query = conn.execute("select * from Alunos")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        for i in result:
            if username == i['Username']:
                return i
        pass

    def getAlunoByName(name):
        conn = db_connect.connect()
        query = conn.execute("select * from Alunos")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        for i in result:
            if name == i['Nome']:
                return i
        pass

class QueueAlunos(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from QueueAluno where QueueID = %d" % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class QueueProfessor(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from QueueProfessor where QueueID = %d" % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)


class QueuePais(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from QueuePais where QueueID = %d" % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)


class StudentLogin(Resource):
    def post(self, user, password):
        aluno = OperatorDb.getAlunoByUsername(user)
        print(aluno)
        if aluno != None:
            if password == aluno['Senha']:
                print('Senha correta')
                return aluno

class TeacherLogin(Resource):
    def post(self, user, password):
        professor = OperatorDb.getProfessorByUsername(user)
        print(professor)
        if professor != None:
            if password == professor['Senha']:
                return professor

class ParentsLogin(Resource):
    def post(self, user, password):
        pais = OperatorDb.getPaisByUsername(user)

        print(pais)

        if pais != None:
            if password == pais['Senha']:
                return pais

class Login(Resource):
    def post(self, user, password):
        aluno = OperatorDb.getAlunoByName(user)
        professor = OperatorDb.getProfessorByName(user)
        pais = OperatorDb.getPaisByName(user)

        print(aluno)
        print(professor)
        print(pais)

        if aluno != None:
            if password == aluno['Senha']:
                print('Senha correta')
                return aluno
        elif professor != None:
            if password == professor['Senha']:
                return professor
        elif pais != None:
            if password == pais['Senha']:
                return pais

class Logout(Resource):
    def post(self):
        self.isAuthenticated= False
        object = {'IsAuthenticated': 'False'}

        return [dict(zip(tuple(object.keys()), i)) for i in object]

class Alunos(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from Alunos")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class AlunoById(Resource):
    def get(self, id):
        return jsonify(OperatorDb.getAlunoById(self, id))

        # conn = db_connect.connect()
        # query = conn.execute("select * from Alunos where AlunosId =%d" % int(id))
        # result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        # return jsonify(result)

class ProfessoresContactsPais(Resource):
    def get(self, id):

        conn = db_connect.connect()
        query = conn.execute("select * from Turma_has_Professores where ProfessoresId = %d" % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        turmaId = result[0]['TurmaId']
        query = conn.execute("select * from Alunos_has_Pais where TurmaId = %d" % int(turmaId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        finalResult = []

        for aluno_has_pais in result:
            paisId = aluno_has_pais['PaisID']

            query = conn.execute("select * from Pais where PaisId = %d" % int(paisId))
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

            result[0]['Senha'] = ''

            if result[0] not in finalResult:
                finalResult.append(result[0])


        return jsonify(finalResult)

class ProfessoresContactsById(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from Turma_has_Professores where ProfessoresId = %d" % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        turmaId = result[0]['TurmaId']
        query = conn.execute("select * from Alunos where TurmaId = %d" % int(turmaId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        result[0]['Senha'] = ''

        return jsonify(result)

class PaisContactsById(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from Pais where PaisId = %d" % int(id))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        paisId = result[0]['PaisId']
        query = conn.execute("select * from Alunos_has_Pais where PaisId = %d" % int(paisId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        turmaId = result[0]['TurmaId']
        query = conn.execute("select * from Turma_has_Professores where TurmaId = %d" % int(turmaId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        finalResult = []

        for value in result:
            professorId = value['ProfessoresId']
            query = conn.execute("select * from Professores where ProfessoresId = %d" % int(professorId))

            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

            result[0]['Senha'] = ''

            finalResult.append(result[0])

        return jsonify(finalResult)

class AlunosContactById(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from Alunos where AlunosId = %d" % int(id))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        turmaId = result[0]['TurmaId']
        query = conn.execute("select * from Turma_has_Professores where TurmaId = %d" % int(turmaId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        professorId = result[0]['ProfessoresId']

        query = conn.execute("select * from Professores where ProfessoresId = %d" % int(professorId))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        result[0]['Senha'] = ''

        return jsonify(result)

class ProfessorSendMessageToAluno(Resource):
    def post(self, remetenteNome, destinatarioId, remetenteId, destinatarioQueueId, message):
        # SELECT queue aluno from DB
        conn = db_connect.connect()
        query = conn.execute("select * from QueueAluno where QueueId = %d" % int(destinatarioQueueId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        queueName = result[0]['Nome']

        newMessage = '{Remetente:' + remetenteNome + ', Mensagem:' + message + '}'

        # RabbitMQ

        credentials = pika.PlainCredentials('admin', 'D!o@4701298')
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',
                                                                       5672,
                                                                       '/',
                                                                       credentials))
        channel = connection.channel()

        channel.queue_declare(queueName,False,True,False,False,None)

        channel.basic_publish(exchange= '',
                              routing_key=queueName,
                              body=newMessage)

        connection.close()

        # Insert Message on DB

        ## VALUES(AlunoId, SchoolId, ProfessorId, Mensagem, Data)
        conn.execute("INSERT INTO CaixaEntradaAlunos VALUES(\'%d\', 0, \'%d\', \'%s\', datetime('now'))" % (int(destinatarioId), int(remetenteId), message))

        ## teste para chegar inclusão
        query = conn.execute("select * from CaixaEntradaAlunos")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        print(result)

        return "success"

class ProfessorSendMessageToPais(Resource):
    def post(self, remetenteNome, destinatarioId, remetenteId, destinatarioQueueId, message):
        # SELECT queue aluno from DB
        conn = db_connect.connect()
        query = conn.execute("select * from QueuePais where QueueId = %d" % int(destinatarioQueueId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        queueName = result[0]['Nome']

        newMessage = '{Remetente:' + remetenteNome + ', Mensagem:' + message + '}'

        # RabbitMQ

        credentials = pika.PlainCredentials('admin', 'D!o@4701298')
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',
                                                                       5672,
                                                                       '/',
                                                                       credentials))
        channel = connection.channel()

        channel.queue_declare(queueName,False,True,False,False,None)

        channel.basic_publish(exchange= '',
                              routing_key=queueName,
                              body=newMessage)

        connection.close()

        # Insert Message on DB

        ## VALUES(AlunoId, SchoolId, ProfessorId, Mensagem, Data)
        conn.execute("INSERT INTO CaixaEntradaPais VALUES(\'%d\', \'%d\',  0, 0,  \'%s\', datetime('now'))" % (int(destinatarioId), int(remetenteId), message))

        ## teste para chegar inclusão
        query = conn.execute("select * from CaixaEntradaPais")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        print(result)

        return "success"


class AlunosSendMessageToProfessores(Resource):
    def post(self, remetenteNome, destinatarioId, remetenteId, destinatarioQueueId, message):
        # SELECT queue aluno from DB
        conn = db_connect.connect()
        query = conn.execute("select * from QueueProfessor where QueueId = %d" % int(destinatarioQueueId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        queueName = result[0]['Nome']

        newMessage = '{Remetente:' + remetenteNome + ', Mensagem:' + message + '}'

        # RabbitMQ

        credentials = pika.PlainCredentials('admin', 'D!o@4701298')
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',
                                                                       5672,
                                                                       '/',
                                                                       credentials))
        channel = connection.channel()

        channel.queue_declare(queueName, False, True, False, False, None)

        channel.basic_publish(exchange='',
                              routing_key=queueName,
                              body=newMessage)

        connection.close()

        # Insert Message on DB

        ## VALUES(ProfessorId, SchoolId, PaisId, AlunosId, Mensagem, Data)
        conn.execute("INSERT INTO CaixaEntradaProfessores VALUES(\'%d\', 0, 0, \'%d\', \'%s\', datetime('now'))" % (int(destinatarioId), int(remetenteId), message))

        return "success"

class PaisSendMessageToProfessores(Resource):
    def post(self, remetenteNome, destinatarioId, remetenteId, destinatarioQueueId, message):
        # SELECT queue aluno from DB
        conn = db_connect.connect()
        query = conn.execute("select * from QueueProfessor where QueueId = %d" % int(destinatarioQueueId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        queueName = result[0]['Nome']

        newMessage = '{Remetente:' + remetenteNome + ', Mensagem:' + message + '}'

        # RabbitMQ

        credentials = pika.PlainCredentials('admin', 'D!o@4701298')
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',
                                                                       5672,
                                                                       '/',
                                                                       credentials))
        channel = connection.channel()

        channel.queue_declare(queueName, False, True, False, False, None)

        channel.basic_publish(exchange='',
                              routing_key=queueName,
                              body=newMessage)

        connection.close()

        # Insert Message on DB
        ## VALUES(ProfessorId, SchoolId, PaisId, AlunosId, Mensagem, Data)
        conn.execute("INSERT INTO CaixaEntradaProfessores VALUES(\'%d\', 0, \'%d\', 0, \'%s\', datetime('now'))" % (int(destinatarioId), int(remetenteId), message))

        return "success"

class AlunosGetMessages(Resource):
    def get(self, alunoId):
        conn = db_connect.connect()
        query = conn.execute("select * from CaixaEntradaAlunos where AlunoId = %d" % int(alunoId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        return result


class ProfessoresGetMessages(Resource):
    def get(self, professoresId):
        conn = db_connect.connect()
        query = conn.execute("select * from CaixaEntradaProfessores where ProfessoresId = %d" % int(professoresId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        return result

class PaisGetMessages(Resource):
    def get(self, paisId):
        conn = db_connect.connect()
        query = conn.execute("select * from CaixaEntradaPais where PaisId = %d" % int(paisId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        return result

# LOGIN/LOGOUT
api.add_resource(StudentLogin, '/login/students/<user>/<password>')
api.add_resource(ParentsLogin, '/login/parents/<user>/<password>')
api.add_resource(TeacherLogin, '/login/teacher/<user>/<password>')

api.add_resource(QueueAlunos, '/alunos/queue/<id>')
api.add_resource(QueuePais, '/pais/queue/<id>')
api.add_resource(QueueProfessor, '/professores/queue/<id>')

api.add_resource(Alunos, '/alunos')
api.add_resource(AlunoById, '/alunos/<id>')
api.add_resource(AlunosContactById, '/alunos/<id>/contacts')
api.add_resource(PaisContactsById, '/pais/<id>/contacts')
api.add_resource(ProfessoresContactsById, '/professores/<id>/contacts/alunos')
api.add_resource(ProfessoresContactsPais, '/professores/<id>/contacts/pais')

## Endpoints Send Messages
api.add_resource(ProfessorSendMessageToAluno, '/professor/send/alunos/<remetenteNome>/<destinatarioId>/<remetenteId>/<destinatarioQueueId>/<message>')
api.add_resource(ProfessorSendMessageToPais, '/professor/send/pais/<remetenteNome>/<destinatarioId>/<remetenteId>/<destinatarioQueueId>/<message>')
api.add_resource(AlunosSendMessageToProfessores, '/alunos/send/professores/<remetenteNome>/<destinatarioId>/<remetenteId>/<destinatarioQueueId>/<message>')
api.add_resource(PaisSendMessageToProfessores, '/pais/send/professores/<remetenteNome>/<destinatarioId>/<remetenteId>/<destinatarioQueueId>/<message>')

## Endpoints Get Messages
api.add_resource(AlunosGetMessages, '/alunos/messages')
api.add_resource(ProfessoresGetMessages, '/professor/messages')
api.add_resource(PaisGetMessages, '/pais/messages')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
