from zabbix_utils import Sender


# abbix_sender -z sa-sp1-be-pool-1.monitoracao.sasp1.oci.i.globo -p 10003 -s "teste_sender_oci" -k grafana_payload -o "teste"


sender = Sender(server='sa-sp1-be-pool-1.monitoracao.sasp1.oci.i.globo', port=10003)
resp = sender.send_value('teste_sender_oci', 'grafana_payload', "teste python")

print(resp)
