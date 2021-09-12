import os
template = {
    "info": {
        "title": "Hero Surveys API",
        "description": "API for surveys",
        "contact": {
            "responsibleOrganization": "SanJK Tech",
            "email": "rainbook2000@gmail.com",
        },
        "termsOfService": "www.twitter.com/riascosdev",
        "version" : "1.0",
    }, 
    "consumes": [
        "application/json",
    ],
    "produces": [
        "application/json",
    ],
    "host": "https://surveys-api-rest.herokuapp.com" if os.environ.get("FLASK_ENV") != "development" else "localhost:5000",
    "basePath": "/",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer":{
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}


swagger_config = {
    "openapi": "3.0.2",
    "doc_dir": './src/docs',
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
