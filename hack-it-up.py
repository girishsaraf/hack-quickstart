import os
import json
import argparse
import shutil
from jinja2 import Environment, FileSystemLoader

DOCKER_COMPOSE_TEMPLATE = "docker-compose.yml.j2"
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def get_supported_frameworks():
    supported_frameworks_file = os.path.join(os.path.dirname(__file__), "static/supported_stack.json")
    supported_frameworks = json.load(open(supported_frameworks_file))
    return supported_frameworks


def parse_arguments():
    supported_frameworks = get_supported_frameworks()
    parser = argparse.ArgumentParser(
        description="Generate a project structure given a choice of backend, frontend, and database"
    )
    parser.add_argument("--backend", choices=supported_frameworks["backend"], required=True,
                        help="Choose backend framework: " + ", ".join(supported_frameworks["backend"]))
    parser.add_argument("--frontend", choices=supported_frameworks["frontend"], required=True,
                        help="Choose frontend framework: " + ", ".join(supported_frameworks["frontend"]))
    parser.add_argument("--db", choices=supported_frameworks["db"], required=True,
                        help="Choose database: " + ", ".join(supported_frameworks["db"]))
    parser.add_argument("--output", type=str, required=True,
                        help="Output directory for generated project. Give complete path")
    parser.add_argument("--project_name", type=str, required=False,
                        help="Enter project name (optional, helps in Django setup)")
    return parser.parse_args()


def create_output_dir(path):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created output directory: {path}")
        return True
    else:
        print(f"Output directory already exists: {path}")
        return False


def render_template_file(env, template_relative_path, context):
    """Render a single template file given its relative path and context."""
    template = env.get_template(template_relative_path)
    return template.render(context)


def process_template_directory(env, src_dir, dest_dir, context):
    """Recursively process a template directory; render .j2 files, copy others."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_file_path, src_dir)
            dest_file_path = os.path.join(dest_dir, rel_path)
            if file.endswith('.j2'):
                dest_file_path = dest_file_path.rstrip('.j2')
                template_rel_path = os.path.relpath(src_file_path, env.loader.searchpath[0])
                rendered_content = render_template_file(env, template_rel_path, context)
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                with open(dest_file_path, 'w') as f:
                    f.write(rendered_content)
                print(f"Rendered template: {dest_file_path}")
            else:
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                shutil.copy(src_file_path, dest_file_path)
                print(f"Copied file: {dest_file_path}")


def generate_sources():
    args = parse_arguments()

    config = {
        "backend": args.backend,
        "frontend": args.frontend
    }

    output_directory = args.output
    create_project_status = create_output_dir(output_directory)
    if create_project_status:
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

        # Generating Backend Files
        backend_template_dir = os.path.join("backend", args.backend)
        backend_output_dir = os.path.join(output_directory, "backend")
        process_template_directory(env, os.path.join(TEMPLATE_DIR, backend_template_dir), backend_output_dir, config)

        # Generating Frontend Files
        frontend_template_dir = os.path.join("frontend", args.frontend)
        frontend_output_dir = os.path.join(output_directory, "frontend")
        process_template_directory(env, os.path.join(TEMPLATE_DIR, frontend_template_dir), frontend_output_dir, config)

        # Generating Database docker-compose
        database_configuration_file = os.path.join(os.path.dirname(__file__), "static", args.db + "_config.json")
        with open(database_configuration_file) as f:
            database_config = json.load(f)
            config.update(database_config)

        # Generating Docker Compose file
        docker_compose_content = render_template_file(env, DOCKER_COMPOSE_TEMPLATE, config)
        docker_compose_output_path = os.path.join(output_directory, "docker-compose.yml")
        with open(docker_compose_output_path, 'w') as f:
            f.write(docker_compose_content)
        print(f"Generated docker-compose file at: {docker_compose_output_path}")


if __name__ == "__main__":
    generate_sources()
