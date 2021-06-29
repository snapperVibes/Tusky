import os

import click

HERE = os.path.dirname(__file__)
CODEGEN_DIR = os.path.join(HERE, "codegen")
OPENAPI_FILE = os.path.join(CODEGEN_DIR, "openapi.json")
PROTO_FILE = os.path.join(CODEGEN_DIR, "users.proto")
JS_DIR = os.path.join(CODEGEN_DIR, "js")
PYTHON_DIR = os.path.join(CODEGEN_DIR, "python")


@click.group()
def cli():
    pass


@click.command()
@click.option("--production/--debug", default=False)
@click.option("--warning/--no-warning", default=True)
def runserver(production, warning):
    import uvicorn

    reload = False if production else True
    if warning:
        click.echo(
            "manage.py is currently not a production ready implementation. "
            "A Docker image will be later provided to run the server.\n"
            "The app runs in debug mode unless otherwise specified using the `--production` option."
        )
    uvicorn.run("server:app", reload=reload)


def generate_openapi():
    import json
    from server import app

    content = app.openapi()
    with open(OPENAPI_FILE, "w") as f:
        json.dump(content, f)


def generate_protobufs():
    # This is a terrible way to create protobufs.
    # However, I am happy with a hacky solution that works.
    import subprocess

    subprocess.run(f"openapi2proto -spec {OPENAPI_FILE} -annotate -out {PROTO_FILE}")
    subprocess.run(
        f"protoc "
        f"--proto_path=. "
        f"--js_out={JS_DIR} "
        f"--python_out={PYTHON_DIR} "
        f"{PROTO_FILE}"
    )
    import grpc_tools.protoc

    grpc_tools.protoc.main(
        (
            f"--python_out={PYTHON_DIR} ",
            f"--grpc_python_out={PYTHON_DIR}",
            PROTO_FILE,
        )
    )


def remove_codegen_files():
    for root, dirs, files in os.walk(CODEGEN_DIR):
        if "google" in root:
            continue
        for file in files:
            if file != ".gitignore":
                os.remove(os.path.join(root, file))


@click.command()
@click.option("--rm/--create", default=False)
def codegen(rm):
    if rm:
        remove_codegen_files()

    else:
        # Normal operation: gen code
        # https://raw.githubusercontent.com/googleapis/googleapis/master/google/api/annotations.proto
        # https://raw.githubusercontent.com/googleapis/googleapis/master/google/api/http.proto

        generate_openapi()
        generate_protobufs()


@click.command()
def create_user():
    from codegen.python.codegen import users_pb2 as users

    r = users.GetUserRequest()
    print(r.__dir__())


cli.add_command(runserver)
cli.add_command(codegen)
cli.add_command(create_user)


if __name__ == "__main__":
    cli()
