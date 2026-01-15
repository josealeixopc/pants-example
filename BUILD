file(
    name="app",
    source="app.py",
)

shell_source(
    name="generate_requirements_script",
    source="generate_requirements.sh",
)

package_v2_shell_command(
    name="generate-requirements-v2",
    command="./generate_requirements.sh",
    output_files=["requirements.txt"],
)

docker_image(
    name="hello-world-app",
    repository="hello-world",
    dependencies=[
        ":app",
        ":generate-requirements-v2",
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
