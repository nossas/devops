import docker


docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')


def get_docker_services_choices():
    # lazy(get_status_choices, tuple)()
    containers = docker_client.containers.list(
        all=True #, filters={"name": ["bonde", "cms", "whoami"]}
    )
    return [("", ""),] + [
        (f"{container.name}@docker", container.name) for container in containers
    ]