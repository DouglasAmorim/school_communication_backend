from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
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

            finalResult.append(result)

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

        result[0]['Senha'] = ''

        return jsonify(result)

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


# LOGIN/LOGOUT ENDPOINTS
#api.add_resource(Login, '/login/<user>/<password>')
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
