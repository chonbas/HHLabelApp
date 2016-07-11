#!/usr/bin/python
from app import *

application = create_app('production')

if __name__ == "__main__":
	application.run()
