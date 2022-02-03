from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps


db_connect = create_engine('sqlite:///db_scholl_app.sqlite')
app = Flask(__name__)
api = Api(app)

class Alunos(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from Alunos")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class AlunoById(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from Alunos where AlunosId =%d" % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)


class ContactById(Resource):
    def get(self, id):
        conn = db_connect.connect()
        query = conn.execute("select * from Alunos where AlunosId = %d" % int(id))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        turmaId = result[0]['TurmaId']
        query = conn.execute("select * from Turma_has_Professores where TurmaId = %d" % int(turmaId))

        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        professorId = result[0]['ProfessoresId']

        print(professorId)

        query = conn.execute("select * from Professores where ProfessoresId = %d" % int(professorId))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]

        print(result)

        return jsonify(result)


api.add_resource(Alunos, '/alunos')
api.add_resource(AlunoById, '/alunos/<id>')
api.add_resource(ContactById, '/alunos/<id>/contacts')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
