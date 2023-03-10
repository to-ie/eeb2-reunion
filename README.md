# EEB2 reunion

## Table of content
- [About the project](#about-the-project)
  * [Screenshots](#screenshots)
  * [Tech Stack](#tech-stack)
- [Getting started](#getting-started)
  * [Local variables](#local-variables)
  * [Run locally](#run-locally)
  * [Deployment](#deployment)
  * [Other commands](#other-commands)
- [Contributing](#contributing) 
- [FAQ](#faq)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## About the Project
In 2025, it will be 20 years since we graduated from high school. This calls for celebrations!

Some people started getting people together via a WhatsApp group, and this made me realise that we might need a more robust way of managing the RSVPs. We have all the names of the students in the Bac Book, all we are missing is their contact details, to reach out. 

This platform aims to:
1. Spread the word about the event.
2. Help collect contact details of past classmates.


### Screenshots
<img src="https://github.com/to-ie/eeb2-reunion/blob/main/app/static/mock.jpg?raw=true" width="600px" />


### Tech Stack

<details>
  <summary>Web app</summary>
  <ul>
    <li><a href="https://www.typescriptlang.org/](https://flask.palletsprojects.com/en/2.2.x/">Python Flask</a></li>
    <li><a href="https://getbootstrap.com/docs/3.4/css/">Bootstrap CSS</a></li>
  </ul>
</details>

<details>
<summary>Database</summary>
  <ul>
    <li><a href="https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/">Flask SQL Alchemy</a></li>
    <li><a href="https://www.mysql.com/">MySQL</a></li>
  </ul>
</details>

## Getting Started

### Local variables
```
SECRET_KEY = 
SQLALCHEMY_DATABASE_URI = 
SQLALCHEMY_TRACK_MODIFICATIONS = 

UPLOAD_EXTENSIONS = 
MAX_CONTENT_LENGTH = 
UPLOAD_PATH = 

MAIL_SERVER = 
MAIL_PORT = 
MAIL_USE_TLS = 
MAIL_USERNAME = 
MAIL_PASSWORD = 
ADMINS = 
```

### Run Locally

Clone the project

```bash
  git clone https://github.com/to-ie/eeb2-reunion
```

Go to the project directory

```bash
  cd eeb2-reunion
```

Activate virtual environment

```bash
Linux:
source venv/bin/activate

Windows: 
venv\Scripts\activate
```

Install dependencies

```bash
pip install requirements.txt
```

Run locally: 
```
flask run
```

### Other commands
Database migration:
```
flask db migrate -m "posts table"
flask db upgrade
```

Set Debug mode:
```
export FLASK_DEBUG=1
```

Update app:
```
(venv) $ git pull                              # download the new version
(venv) $ sudo supervisorctl stop reunion       # stop the current server
(venv) $ flask db upgrade                      # upgrade the database
(venv) $ flask translate compile               # upgrade the translations
(venv) $ sudo supervisorctl start reunion      # start a new server
```


**Other:** 
* [ ] Organise the event (who?)

## Contributing

Contributions are always welcome! Get in touch if you are not sure how you can help! 

If you want to help out with the technical side of this project, pull requests are the simplest way.

## FAQ

- Why?
  + It will be 20 years since we graduated, surely it's important to mark the day?

## License

Distributed under the [MIT License](https://choosealicense.com/licenses/mit/).

## Contact

Theo - hello@t-o.ie

## Acknowledgements

Useful resources and libraries that we have used in this project:

 - [Awesome Readme Template](https://github.com/Louis3797/awesome-readme-template)
 - [Flask](https://flask.palletsprojects.com/en/2.2.x/)

