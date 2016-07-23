# HHLabelApp
Tool being developed by HackHarassment to crowd-source data labeling, as well as help collect data to understand how different members of the online community perceive harassment.

## Development

HHLabelApp uses Python 2.7 and is built using the Flask web framework. To get started simply create a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), activate it, and execute the following commands:

```shell
$ git clone https://github.com/HackHarassment/HHLabelApp.git
$ cd HHLabelApp
$ pip install -r requirements.txt
$ python manage.py start_db
$ python manage.py runserver
```

# Files Included:
manage.py - framework to manage development environment/localhosting
config.py - configuration file, split into different classes, specifying the app's configuration
app/ - Primary app folder
app/models.py - Database model definitions
app/__init__.py - initialization file for application
app/static - static resources
app/static/templates/index.html - AngularJS Single Page Application- ie, the client/front-end
app/static/components/ - All the AngularJS components, and associated controllers and templates, utilized by the single page app
app/static/css - Custom style sheet
app/static/images - Images
app/static/api/views.py - Route definitions for the REST API
app/static/auth/views.py - Route definitions to handle logins/registrations as part of our REST API
 
