file(
    name="app",
    source="app.py",
)

shell_source(
    name="generate_requirements_script",
    source="generate_requirements.sh",
)

package_shell_command(
    name="generate-requirements",
    command="./generate_requirements.sh",
    execution_dependencies=[":generate_requirements_script"],
    output_files=["requirements.txt"],
)

docker_image(
    name="hello-world-app",
    repository="hello-world",
    dependencies=[
        ":app",
        ":generate-requirements",
    ],
)

# file(
#     name="requirements",
#     source="requirements.txt",
# )

# docker_image(
#     name="hello-world-app-requirements-already-generated",
#     repository="hello-world",
#     dependencies=[
#         ":app",
#         ":requirements",
#     ],
# )
