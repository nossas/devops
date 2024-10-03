from flask import Flask, render_template, request, redirect, url_for
import urllib
import boto3

app = Flask(__name__)

# Configurar o boto3 para se conectar ao LocalStack
route53 = boto3.client(
    'route53',
    endpoint_url='http://localhost:4566',  # LocalStack URL
    region_name='us-east-1',  # Região (pode ser qualquer uma)
    aws_access_key_id='fake-access-key',  # Chaves falsas para LocalStack
    aws_secret_access_key='fake-secret-key'
)

@app.route('/', methods=['GET', 'POST'])
def list_hosted_zones():
    """Lista todas as Hosted Zones"""

    if request.method == 'POST' and "external_id" in request.form and request.form["external_id"]:
        external_id = request.form['external_id']  # Identificador externo para filtrar

        # Obtém todas as Hosted Zones
        response = route53.list_hosted_zones()
        hosted_zones = response.get('HostedZones', [])

        # Lista de Hosted Zones que correspondem ao identificador externo
        filtered_zones = []
        for zone in hosted_zones:
            zone_id = zone['Id'].split('/')[-1]  # Apenas a parte final do ID

            # Obtém as tags da zona
            tags_response = route53.list_tags_for_resource(
                ResourceType='hostedzone',
                ResourceId=zone_id
            )
            tags = tags_response.get('ResourceTagSet', {}).get('Tags', [])

            # Verifica se a tag 'ExternalIdentifier' corresponde ao valor fornecido
            for tag in tags:
                if tag['Key'] == 'ExternalIdentifier' and tag['Value'] == external_id:
                    filtered_zones.append(zone)
                    break
        
        return render_template('zones.html', hosted_zones=filtered_zones)

    response = route53.list_hosted_zones()
    hosted_zones = response.get('HostedZones', [])

    # Codificar o ID das zonas para serem usados na URL
    for zone in hosted_zones:
        zone_id = zone['Id'].split('/')[-1]  # Pega apenas a parte final do ID
        zone['EncodedId'] = urllib.parse.quote(zone_id)  # Codifica o ID sem a parte '/hostedzone/'

    return render_template('zones.html', hosted_zones=hosted_zones)

@app.route('/records/<zone_id>')
def list_records(zone_id):
    """Lista os registros DNS de uma Hosted Zone"""
    decoded_zone_id = urllib.parse.unquote(zone_id)
    full_zone_id = f'/hostedzone/{decoded_zone_id}'

    # Obtém os registros DNS da Hosted Zone
    response = route53.list_resource_record_sets(HostedZoneId=full_zone_id)
    records = response.get('ResourceRecordSets', [])
    
    return render_template('records.html', records=records)

@app.route('/create', methods=['POST'])
def create_hosted_zone():
    """Cria uma nova Hosted Zone"""
    zone_name = request.form['zone_name']  # Obtém o nome da zona do formulário
    external_id = request.form['external_id']  # Identificador externo, por exemplo 'project_id'

    # Cria a Hosted Zone no Route53
    response = route53.create_hosted_zone(
        Name=zone_name,
        CallerReference=str(hash(zone_name))  # Referência única (pode ser UUID)
    )

    # Adiciona a tag com o identificador externo à Hosted Zone
    zone_id = response['HostedZone']['Id']
    route53.change_tags_for_resource(
        ResourceType='hostedzone',
        ResourceId=zone_id.split('/')[-1],  # Apenas a parte final do ID
        AddTags=[
            {'Key': 'ExternalIdentifier', 'Value': external_id}
        ]
    )

    return redirect(url_for('list_hosted_zones'))

@app.route('/delete/<zone_id>', methods=['POST'])
def delete_hosted_zone(zone_id):
    """Exclui uma Hosted Zone"""
    # Decodifica o ID da zona
    decoded_zone_id = urllib.parse.unquote(zone_id)
    
    # Exclui a Hosted Zone pelo ID completo ('/hostedzone/<ID>')
    full_zone_id = f'/hostedzone/{decoded_zone_id}'
    route53.delete_hosted_zone(Id=full_zone_id)

    return redirect(url_for('list_hosted_zones'))


@app.route('/containers')
def list_services():
    import docker

    # Conectar ao cliente Docker utilizando o socket Docker montado no container
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    # Obter e inspecionar um container
    try:
        # import ipdb;ipdb.set_trace()
        containers = client.containers.list(all=True, filters={"name": ["bonde", "cms"]})
        return render_template('containers.html', containers=containers)
    # except docker.errors.NotFound:
        # print(f"Container '{container_name}' não encontrado.")
    except Exception as e:
        print(f"Erro: {e}")

    return render_template('containers.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
