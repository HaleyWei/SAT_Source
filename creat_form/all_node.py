# coding:utf-8
from joern.all import JoernSteps
import db_search as search
from py2neo.packages.httpstream import http
http.socket_timeout = 9999


def all_node(db):
    query = 'g.V()'
    result = db.runGremlinQuery(query)
    for r in result:
        print r


if __name__ == '__main__':
    j = JoernSteps()
    j.connectToDatabase()
    all_node(j)
