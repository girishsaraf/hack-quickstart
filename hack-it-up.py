import os
import argparse
import shutil
from jinja2 import Environment, FileSystemLoader

DOCKER_COMPOSE_TEMPLATE = "docker-compose.yml.j2"
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate a fullstack project scaffold with specified backend, frontend, and database."
    )
    parser.add_argument("--backend", choices=["flask", "django"], required=True,
                        help="Choose backend framework: flask or django")
    parser.add_argument("--frontend", choices=["react", "angular", "nextjs"], required=True,
                        help="Choose frontend framework: react, angular, or nextjs")
    parser.add_argument("--db", choices=["mysql", "postgres"], required=True,
                        help="Choose database: mysql or postgres")
    parser.add_argument("--output_dir", type=str, required=True,
                        help="Output directory for generated project")
    return parser.parse_args()


def create_output_dir(path):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created output directory: {path}")


def map_database_config(db_type):
    """Map database type to its docker image and port."""
    db_configs = {
        "mysql": {"image": "mysql:latest", "port": 3306},
        "postgres": {"image": "postgres:latest", "port": 5432},
    }
    return db_configs[db_type]


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
        "frontend": args.frontend,
        **map_database_config(args.db),
    }

    output_directory = args.output_dir
    create_output_dir(output_directory)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    backend_template_dir = os.path.join("backend", args.backend)
    backend_output_dir = os.path.join(output_directory, "backend")
    process_template_directory(env, os.path.join(TEMPLATE_DIR, backend_template_dir), backend_output_dir, config)

    frontend_template_dir = os.path.join("frontend", args.frontend)
    frontend_output_dir = os.path.join(output_directory, "frontend")
    process_template_directory(env, os.path.join(TEMPLATE_DIR, frontend_template_dir), frontend_output_dir, config)

    docker_compose_content = render_template_file(env, DOCKER_COMPOSE_TEMPLATE, config)
    docker_compose_output_path = os.path.join(output_directory, "docker-compose.yml")
    with open(docker_compose_output_path, 'w') as f:
        f.write(docker_compose_content)
    print(f"Generated docker-compose file at: {docker_compose_output_path}")


if __name__ == "__main__":
    generate_sources()
