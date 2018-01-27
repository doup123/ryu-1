from elasticsearch import Elasticsearch
es=Elasticsearch()
result=es.search(index="logstash-2018.01.26",size=10000,body={"query":{"match": {"event_type": "ssh" }}})
malicious_ips=[]
for i in result['hits']['hits']:
    malicious_ips.append(i['_source']['src_ip'])
mal_ip=list(map(lambda x: str(x)+"/32",malicious_ips))
unique_only=set(mal_ip)