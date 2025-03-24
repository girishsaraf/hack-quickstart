import os
import argparse
import shutil
from jinja2 import Environment, FileSystemLoader

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
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created output directory: {path}")

def render_template_file(env, template_relative_path, context):
    """
    Render a single template file given its relative path (from the templates root)
    and the context dictionary.
    """
    template = env.get_template(template_relative_path)
    return template.render(context)

def process_template_directory(env, src_dir, dest_dir, context):
    """
    Recursively process a template directory, rendering .j2 files and copying non-template files.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file_path = os.path.join(root, file)
            # Determine the relative path with respect to the source directory
            rel_path = os.path.relpath(src_file_path, src_dir)
            dest_file_path = os.path.join(dest_dir, rel_path)
            
            # Check if file is a Jinja2 template (ends with .j2)
            if file.endswith('.j2'):
                # Remove the .j2 extension for the output file
                dest_file_path = dest_file_path[:-3]
                # Construct the template path relative to the templates folder.
                # Note: env.loader.searchpath[0] is the base template directory.
                template_rel_path = os.path.relpath(src_file_path, env.loader.searchpath[0])
                rendered_content = render_template_file(env, template_rel_path, context)
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                with open(dest_file_path, 'w') as f:
                    f.write(rendered_content)
                print(f"Rendered template: {dest_file_path}")
            else:
                # Copy static file directly
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                shutil.copy(src_file_path, dest_file_path)
                print(f"Copied file: {dest_file_path}")

def main():
    args = parse_arguments()
    
    # Build configuration from arguments
    config = {
        "backend": args.backend,
        "frontend": args.frontend,
        "db_type": args.db,
    }
    
    # Map database option to image and port
    if args.db == "mysql":
        config["db_image"] = "mysql:latest"
        config["db_port"] = 3306
    elif args.db == "postgres":
        config["db_image"] = "postgres:latest"
        config["db_port"] = 5432
    
    output_dir = args.output_dir
    create_output_dir(output_dir)
    
    # Set up the Jinja2 environment; assumes your templates are in a folder called "templates"
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Process backend templates
    backend_template_dir = os.path.join("backend", args.backend)
    backend_output_dir = os.path.join(output_dir, "backend")
    process_template_directory(env, os.path.join(template_dir, backend_template_dir), backend_output_dir, config)
    
    # Process frontend templates
    frontend_template_dir = os.path.join("frontend", args.frontend)
    frontend_output_dir = os.path.join(output_dir, "frontend")
    process_template_directory(env, os.path.join(template_dir, frontend_template_dir), frontend_output_dir, config)
    
    # Render the docker-compose file (assumed to be directly under the templates folder)
    docker_compose_template = "docker-compose.yml.j2"
    docker_compose_content = render_template_file(env, docker_compose_template, config)
    docker_compose_output_path = os.path.join(output_dir, "docker-compose.yml")
    with open(docker_compose_output_path, 'w') as f:
        f.write(docker_compose_content)
    print(f"Generated docker-compose file at: {docker_compose_output_path}")

if __name__ == "__main__":
    main()
