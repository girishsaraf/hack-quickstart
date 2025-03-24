# Fullstack Project Generator

## Overview

The Fullstack Project Generator is a command-line tool designed to scaffold a full-stack application using Docker. It supports multiple backend frameworks, frontend frameworks, and databases. Based on your input, the generator creates a project structure that includes:

- A **backend** service (using either Flask, FastAPI, or Django).
- A **frontend** service (using React, Angular, or Next.js).
- A **database** service (using MySQL or PostgreSQL).
- A complete **Docker Compose** setup that ties all these services together.

This tool is modular and extensible—new frameworks or services can easily be added by introducing new templates.

## Supported Technologies

| Component | Supported Options               |
|-----------|---------------------------------|
| **Backend**   | Flask, Django, FastAPI       |
| **Frontend**  | React, Angular, Next.js      |
| **Database**  | MySQL, PostgreSQL            |

## Features

- **Modular Templates:** Each service has its own template directory with Jinja2 files (`.j2`) that can be rendered based on user-specified options.
- **Dynamic Docker Compose:** The generator creates a `docker-compose.yml` file that automatically configures the selected services.
- **Customizable Output:** Specify your output directory to generate a fully-scaffolded project.
- **Extensible:** Easily add support for new frameworks or technologies by adding new template folders and updating the generator.

## Prerequisites

- **Python 3.6+**  
- **Jinja2** for template rendering  
  Install via pip:
  ```bash
  pip install jinja2


# Template Rendering Tool

This Python script is designed to render templates for a project, leveraging custom configurations and database mappings. The main goal is to process template files and directories to generate final outputs based on a user-defined structure.

## Features

- **CLI Argument Parsing**: Configurable run options via parsing command-line arguments.
- **Output Directory Management**: Automatic creation of output directories, ensuring proper storage for the rendered templates.
- **Database Configuration Mapping**: Maps provided database details for use in the rendered templates.
- **Template Rendering**: Processes individual files and directories to render templates with Jinja2 support.
- **Flexible Configuration**: Allows defining templates and where they should be rendered.

## Prerequisites

- Python 3.7 or higher
- `Jinja2` python library (For rendering templates)

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

_Ensure the `requirements.txt` includes all necessary dependencies like `jinja2`._

## Usage

Run the script from the command line using Python. Example:

```bash
python script_name.py --template /path/to/templates --output /path/to/output --db-config /path/to/db_config.json
```

### Command-line Arguments

- **`--template`**: Path to the directory containing the template files.  
- **`--output`**: Path to the generated output files.  
- **`--db-config`**: JSON file containing database configurations to inject into the templates.  

### Example

```bash
python script_name.py \
    --template ./templates \
    --output ./output \
    --db-config ./database.json
```

This will process the templates in the `./templates` directory, applies the configurations from `./database.json`, and output the rendered templates into the `./output` directory.

## Code Structure Overview

- **Constants**
  - `DOCKER_COMPOSE_TEMPLATE`: Defines the base Docker compose file template used in the application.
  - `TEMPLATE_DIR`: Specifies the default directory to look for the templates.

- **Functions**
  - `parse_arguments`: Handles the command-line argument parsing to retrieve `--template`, `--output`, and `--db-config`.
  - `create_output_dir`: Ensures the output directory exists, creating it if necessary.
  - `map_database_config`: Reads and maps the database configuration file to use for rendering templates.
  - `render_template_file`: Renders a single template file using Jinja2.
  - `process_template_directory`: Processes the entire directory of template files and creates the corresponding output files.
  - `main`: The entry point that ties together argument parsing, database mapping, template rendering, and directory processing.

## Output

After execution, the tool will produce rendered template files in the specified output directory.

## Contributing

If you'd like to contribute:

1. Fork the repository
2. Create a new branch (`feature/my-feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- Built with Python and Jinja2.

---

Feel free to adjust the `README.md` file as necessary depending on additional functionality your script provides or additional libraries it depends on.