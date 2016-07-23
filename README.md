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
<ul>
<li>manage.py - framework to manage development environment/localhosting</li>
<li>config.py - configuration file, split into different classes, specifying the app's configuration</li>
<li>app/ - Primary app folder</li>
<li>app/models.py - Database model definitions</li>
<li>app/_init_.py - initialization file for application</li>
<li>app/static - static resources</li>
<li>app/static/templates/index.html - AngularJS Single Page Application- ie, the client/front-end</li>
<li>app/static/components/ - All the AngularJS components, and associated controllers and templates, utilized by the single page app</li>
<li>app/static/css - Custom style sheet</li>
<li>app/static/images - Images</li>
<li>app/static/api/views.py - Route definitions for the REST API</li>
<li>app/static/auth/views.py - Route definitions to handle logins/registrations as part of our REST API</li>
 </ul>
