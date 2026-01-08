# pants-example

An example project using [Pants Build System](https://www.pantsbuild.org/) to create a simple Python application packaged in a Docker image, that relies on a generated `requirements.txt` file.

## Current behavior

### Empty requirements.txt in Docker image

Running the following command, I'd expect the `requirements.txt` file to be generated and included in the Docker image:

```bash
PANTS_DOCKER_BUILD_NO_CACHE=True pants --no-pantsd package :hello-world-app
```

However, upon inspecting the generated Docker image, I find that the `requirements.txt` file is empty:

```bash
docker run --rm -it hello-world:latest bash
# cat requirements.txt
# (empty file)
```

But if I generate the files beforehand:

```bash
./generate_requirements.sh
```

And then build the Docker target that uses the pre-generated `requirements.txt`:

```bash
PANTS_DOCKER_BUILD_NO_CACHE=True pants --no-pantsd package :hello-world-app-requirements-already-generated
```

The `requirements.txt` file is correctly populated in the Docker image.

### Generated file is not output to the repository directory

Another behavior that I'd like to achieve is for the `generate-requirements` target to generate the `requirements.txt` file directly in the repository directory. This would allow me to inspect the generated file directly in my working directory after running the generation target, or anything that depends on it.
