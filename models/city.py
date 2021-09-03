import os
from builtins import classmethod, int
from datetime import datetime

from models.state import State
from es import es


class City:
    def __init__(self):
        pass

    @classmethod
    def list(cls, state):
        if state != "":
            city_data = es.search(
                index=os.environ.get("INDEX"),
                body={
                    'size': 10000,
                    'query': {"bool": {"must": [ {"match": {"state": state}}]}}
                },
                filter_path=['hits.hits._id', 'hits.hits._source', 'hits.hits._parent']
            )
        else:
            city_data = es.search(
                index=os.environ.get("INDEX"),
                body={
                    'size': 10000
                },
                filter_path=['hits.hits._id', 'hits.hits._source', 'hits.hits._parent']
            )
        cities = []
        parent_map = dict()
        if 'hits' in city_data and 'hits' in city_data['hits']:
            for data in city_data['hits']['hits']:
                if data['_source']['relation_type']['name'] == 'state':
                    parent_map[data["_id"]] = data["_source"]["name"]
            cities = [
                {"id": data["_id"], "name": data["_source"]["name"],
                 "state": parent_map.get(data['_source']['relation_type']['parent'], '-')}
                if data['_source']['relation_type']['name'] == 'city' else None
                for data in city_data['hits']['hits']
            ]
            cities = [city for city in cities if city]
        return cities

    @classmethod
    def get(cls, id):
        city_data = es.search(index=os.environ.get("INDEX"),
                              body={'query': {"bool": {"must": [{'match': {'_id': id}},
                                                                   ]}}})
        if 'hits' in city_data and 'hits' in city_data['hits']:
            return {"id": city_data['hits']['hits'][0]['_id'],
                    "name": city_data['hits']['hits'][0]["_source"]["name"],
                    "state_id": city_data['hits']['hits'][0]["_source"]["relation_type"]['parent']}
        return False

    @classmethod
    def create(cls, name, state):
        state_rec = State.get(state)
        if state_rec:
            parent_id = state_rec['id']

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

            body = {"name":name, "relation_type":{ "name":"city", "parent":parent_id } }
            param = {"routing": state}
            res = es.index(index=os.environ.get("INDEX"), id=id, body=body, params = param)
            if "created" in res and res["created"]:
                return True
        return False

    @classmethod
    def edit(cls, id, name, state):
        state_rec = State.get(state)
        if state_rec:
            body = {"name":name, "relation_type":{ "name":"city", "parent":state_rec['id'] } }
            param = {"routing": state}
            res = es.index(index=os.environ.get("INDEX"), id=id, body=body, params = param)
            if "result" in res and res["result"] == "updated":
                return True
        return False

    @classmethod
    def delete(cls, id, state):
        city_rec = City.get(id)
        if city_rec:
            res = es.delete(index=os.environ.get("INDEX"), doc_type='city', id=id, parent=state)
            if "found" in res and res["found"] and "result" in res and res["result"] == "deleted":
                return True
        return False
