from __future__ import absolute_import, print_function

from decimal import Decimal
from datetime import date

from pony.orm.core import *
from pony.orm.serialization import to_dict
from flask import Flask
from flask_restful import Resource, Api
from flask import request
from flask_cors import CORS

db = Database()

#ORM Sets up table relationships
class Risk(db.Entity):
    r_id = PrimaryKey(int, auto=True)
    r_name = Required(str, unique=True)
    field = Set("Field")

class Field(db.Entity):
    f_id = PrimaryKey(int, auto=True)
    f_name = Required(str)
    f_type = Required(str)
    f_r_id = Required(Risk)
    enum = Set("Enum")

class Enum(db.Entity):
    e_id = PrimaryKey(int, auto=True)
    e_name = Required(str)
    e_f_id = Required(Field)

params = dict(
    sqlite=dict(provider='sqlite', filename='bcdatabase.sqlite', create_db=True),
    mysql=dict(provider='mysql', host="britecdb.ceuqzjblxim5.us-east-2.rds.amazonaws.com", port=3306, user="****", passwd="****", db="BriteCDb"),
    postgres=dict(provider='postgres', user='pony', password='pony', host='localhost', database='pony'),
    oracle=dict(provider='oracle', user='c##pony', password='pony', dsn='localhost/orcl')
)

# connect/bind the database
db.bind(**params['mysql'])

# map the tables to database
db.generate_mapping(create_tables=True)

# function - returns specified risk
@db_session
def risk_query(query):

    #Queries database for reveveant rows
    risk = select(r for r in Risk if r.r_id == query)
    fields = select(f for f in Field if f.f_r_id.r_id == query)
    enums = select(e for e in Enum if e.e_f_id.f_r_id.r_id == query)

    #Converts queries to dictionaries
    result = {'risk':[r.to_dict() for r in risk], 'field':[f.to_dict() for f in fields], 'enum': [e.to_dict() for e in enums]}
    return (result)

# function - returns all risks and applicable fields
@db_session
def all_risks():
    risks = select(r for r in Risk)
    result = {'risks': [risk_query(r.r_id) for r in risks]}
    return result

#function - just returns the risks
@db_session
def only_risks():
    risks = select(r for r in Risk)
    result = {'risks': [r.to_dict() for r in risks]}
    return result

#function - grabs all information relating to a single risk
@db_session
def single_risk(riskID):
    result = {'risks': [risk_query(riskID)]}
    return result

#Flask Risk Query API
app = Flask(__name__)
CORS(app)
api = Api(app)

#Gets a single specified risk and its related fields
class Single_Risk(Resource):
    def get(self):
        riskID = request.args.get('rid')
        query = single_risk(riskID)
        return query

#Gets all risks and all fields pertaining to them
class All_Risks(Resource):
    def get(self):
        query = all_risks()
        return query

#Only grabs the risks
class Only_Risks(Resource):
    def get(self):
        query = only_risks()
        return query

#Assigns endpoints for the api resources
api.add_resource(Single_Risk, '/single-risk')
api.add_resource(All_Risks, '/all-risks')
api.add_resource(Only_Risks, '/only-risks')

#Runs the app
if __name__ == '__main__':
    app.run(debug=True)
