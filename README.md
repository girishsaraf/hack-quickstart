# Fullstack Project Generator

## Overview

The Fullstack Project Generator is a command-line tool designed to scaffold a full-stack application using Docker. It supports multiple backend frameworks, frontend frameworks, and databases. Based on your input, the generator creates a project structure that includes:

- A **backend** service (using either Flask or Django).
- A **frontend** service (using React, Angular, or Next.js).
- A **database** service (using MySQL or PostgreSQL).
- A complete **Docker Compose** setup that ties all these services together.

This tool is modular and extensible—new frameworks or services can easily be added by introducing new templates.

## Supported Technologies

| Component | Supported Options               |
|-----------|---------------------------------|
| **Backend**   | Flask, Django                |
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
