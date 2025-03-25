# Fullstack Project Generator

## Overview

The Fullstack Project Generator is a command-line tool designed to generate a full-stack application using Docker. It supports multiple backend frameworks, frontend frameworks, and databases. Based on your input, the generator creates a project structure that includes:

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

## Prerequisites

- **Python 3.6+**  
- **Jinja2** for template rendering  
  Install via pip:
  ```bash
  pip install jinja2
  ```

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

Run the script from the command line using Python. Example:

```bash
python hack-it-up.py --backend <backend> --frontend <frontend> --db <database> --output <output_dir>
```

### Example

```bash
python hack-it-up.py \
    --backend flask \
    --frontend react \
    --db mysql \
    --output /Users/username/Desktop/Projects/my_new_project
```

### Command-line Arguments

- **`--backend`**: Backend choice (Use django, fastapi, flask)  
- **`--frontend`**: Frontend choice (Use react, angular, nextjs)  
- **`--db`**: Database choice (Use mysql / postgres)
- **`--output`**: Path to the generated output directory structure

>[!NOTE]
> Ensure that the output dir is accessible to the code
