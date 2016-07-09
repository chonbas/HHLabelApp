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
