#  CommentsService – Trail Application Microservice

This is a standalone microservice for handling **comments** in the Trail Wellbeing Application. Built using **Python (Flask)**, it connects to a **Microsoft SQL Server** database and provides a fully documented **RESTful API** for creating, reading, updating, and archiving comments related to trails.

#  Project Overview

The CommentsService is part of a larger Trail Application designed to help users explore trails and contribute feedback. This microservice specifically manages:

- Adding new user comments to trails
- Retrieving all active (non-archived) comments
- Allowing users to update their own comments
- Archiving comments (admin-only functionality)

#  deployed at docker hub
https://hub.docker.com/r/samcoakley/commentsservice


# Tech Stack

- **Python 3.11**
- **Flask**
- **Flasgger** (for Swagger UI and API documentation)
- **pyodbc** (ODBC connector for SQL Server)
- **Microsoft SQL Server**
- **Docker** (deployment)

# Files included

-app.py # Main Flask application
-requirements.txt # Python dependencies
-Dockerfile # Docker build config
-README.md # Project documentation


# Author
S. Coakley
University of Plymouth – BSc (Hons) Computer Science
COMP2001 – Web Services and Systems Integration
