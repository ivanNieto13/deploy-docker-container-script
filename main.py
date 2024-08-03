import docker
import time

def deploy_container(image_name, container_name, ports=None, environment=None):
    """
    Deploys a Docker container with the specified image and configuration.

    Parameters:
    - image_name: The name of the Docker image to use.
    - container_name: The name to assign to the container.
    - ports: A dictionary mapping container ports to host ports.
    - environment: A dictionary of environment variables to set in the container.
    """
    client = docker.from_env()

    # Pull the latest version of the image
    print(f"Pulling image {image_name}...")
    client.images.pull(image_name)

    # Stop and remove existing container if it exists
    try:
        existing_container = client.containers.get(container_name)
        print(f"Stopping and removing existing container {container_name}...")
        existing_container.stop()
        existing_container.remove()
    except docker.errors.NotFound:
        print(f"No existing container named {container_name} found. Proceeding to create a new one.")

    # Run the container
    print(f"Creating and starting container {container_name}...")
    container = client.containers.run(
        image_name,
        name=container_name,
        ports=ports,
        environment=environment,
        detach=True
    )

    # Wait for the container to start
    time.sleep(5)

    # Check the container's status
    container.reload()
    print(f"Container {container_name} status: {container.status}")

    if container.status == 'running':
        print(f"Container {container_name} is running successfully.")
    else:
        print(f"Container {container_name} failed to start.")

    return container

# Example usage
if __name__ == "__main__":
    image = "nginx:latest"
    container = "my_nginx_container"
    port_bindings = {80: 8080}  # Map host port 8080 to container port 80
    env_vars = {"MY_ENV_VAR": "value"}  # Example environment variables

    deploy_container(image, container, ports=port_bindings, environment=env_vars)
