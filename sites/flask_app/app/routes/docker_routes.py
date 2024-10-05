from flask import Blueprint, render_template
from flask_login import login_required
import docker

from ..services.etcd_client import etcd_client


docker_routes = Blueprint("docker", __name__, url_prefix="/docker")


@docker_routes.route("/")
@login_required
def list_services():
    # Conectar ao cliente Docker utilizando o socket Docker montado no container
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    # Obter e inspecionar um container
    try:
        containers = client.containers.list(all=True, filters={"name": ["bonde", "cms", "whoami"]})
        # import ipdb;ipdb.set_trace()
        return render_template('containers.html', containers=containers)
    # except docker.errors.NotFound:
        # print(f"Container '{container_name}' não encontrado.")
    except Exception as e:
        print(f"Erro: {e}")

    return render_template('containers.html')