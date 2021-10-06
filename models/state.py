import os
from builtins import classmethod, int
from datetime import datetime

from models.country import Country

from es import es

class State:
    def __init__(self):
        pass

    @classmethod
    def list(cls, country):
        if country != "":
            state_data = es.search(
                index=os.environ.get("INDEX"),
                body={
                    'size': 10000,
                    'query': {"bool": {"must": [ {"match": {"country": country}}]}}
                },
                filter_path=['hits.hits._id', 'hits.hits._source', 'hits.hits._parent']
            )
        else:
            state_data = es.search(
                index=os.environ.get("INDEX"),
                body={
                    'size': 10000
                },
                filter_path=['hits.hits._id', 'hits.hits._source', 'hits.hits._parent']
            )
        states = []
        parent_map = dict()

        if 'hits' in state_data and 'hits' in state_data['hits']:
            for data in state_data['hits']['hits']:
                if data['_source'].get('relation_type') and data['_source']['relation_type']['name'] == 'country':
                    parent_map[data["_id"]] = data["_source"]["name"]

            states = [ {"id": data["_id"], "name": data["_source"]["name"], "country":parent_map.get(data['_source']['relation_type']['parent'], '-')}
                 if data['_source'].get('relation_type') and data['_source']['relation_type']['name']=='state' else None
                for data in state_data['hits']['hits']
            ]
            states = [state for state in states if state]

        return states

    @classmethod
    def get(cls, id):
        state_data = es.search(index=os.environ.get("INDEX"),
                                 body={'query': {"bool": {"must": [{'match': {'_id': id}},
                                                                   ]}}})
        if 'hits' in state_data and 'hits' in state_data['hits']:
            return {"id": state_data['hits']['hits'][0]['_id'],
                    "name": state_data['hits']['hits'][0]["_source"]["name"],
                    "country_id": state_data['hits']['hits'][0]["_source"]["relation_type"]['parent']}
        return False

    @classmethod
    def create(cls, name, country):
        country_rec = Country.get(country)
        if country_rec:
            parent_id = country_rec['id']

            id_data = es.search(index=os.environ.get("INDEX"),
                                body={
                                    "aggs": {
                                        "max_id": {
                                            "max": {
                                                "field": "id"
                                            }
                                        }
                                    },
                                    "size": 0
                                })
            id = id_data['hits']['total']['value'] + 1

            body = {"name":name, "relation_type":{ "name":"state", "parent":parent_id } }
            param = {"routing": country}

            res = es.index(index=os.environ.get("INDEX"), id=str(id), body=body, params = param)
            if "created" in res and res["created"]:
                return True
        return False

    @classmethod
    def edit(cls, id, name, country):
        country_rec = Country.get(country)
        if country_rec:
            body = {"name":name, "relation_type":{ "name":"state", "parent":country_rec['id'] } }
            param = {"routing": country}

            res = es.index(index=os.environ.get("INDEX"), id=str(id), body=body, params = param)

            if "result" in res and res["result"] == "updated":
                return True
        return False

    @classmethod
    def delete(cls, id):
        state_rec = State.get(id)
        if state_rec:
            res = es.delete(index=os.environ.get("INDEX"), id=id)
            if "found" in res and res["found"] and "result" in res and res["result"] == "deleted":
                return True
        return False
