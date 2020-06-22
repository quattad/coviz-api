# the only purpose of this file is to run everything

# __name__ : special string attribute of all python modules
# __main__ : when module is run directly with python -m module_name, module_name becomes __main__
# from api import app
from api import app

if __name__ == "__main__":
    app.run()