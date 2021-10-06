import os
from builtins import classmethod, int
from datetime import datetime
from es import es


class Country:
    def __init__(self):
        pass

    @classmethod
    def list(cls):
        country_data = es.search(index=os.environ.get("INDEX"),
                                 body={'size': 10000},
                                 filter_path=['hits.hits._id', 'hits.hits._source'])
        countries = []
        if 'hits' in country_data and 'hits' in country_data['hits']:
            countries = [{"id": data["_id"], "name": data["_source"]["name"]} if data['_source'].get('relation_type') and data['_source']['relation_type']['name']=='country' else None for data in country_data['hits']['hits'] ]
            countries = [country for country in countries if country]
        return countries

    @classmethod
    def get(cls, id):
        country_data = es.search(index=os.environ.get("INDEX"),
                                 body={'query': {"bool": {"must": [{'match': {'_id': id}}
                                                                   ]}}})
        if 'hits' in country_data and 'hits' in country_data['hits']:
            return {"id": country_data['hits']['hits'][0]['_id'],
                    "name": country_data['hits']['hits'][0]["_source"]["name"]}
        return False

    @classmethod
    def create(cls, name):
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
        id = id_data['hits']['total']['value']+1

        res = es.index(index=os.environ.get("INDEX"), id=id, body={"name": name, "relation_type": {
    "name": "country"
  }})
        if "created" in res and res["created"]:
            return True
        return False

    @classmethod
    def edit_country(cls, id, name):
        res = es.index(index=os.environ.get("INDEX"), id=id, body={"name": name})
        if "result" in res and res["result"] == "updated":
            return True
        return False

    @classmethod
    def delete(cls, id):
        country_rec = Country.get(id)
        if country_rec:
            res = es.delete(index=os.environ.get("INDEX"), id=id)
            if "found" in res and res["found"] and "result" in res and res["result"] == "deleted":
                return True
        return False
