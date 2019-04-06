import os

LOCAL = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db = LOCAL + '\\db\\'
resources = LOCAL + '/resources/'

db_file = db.replace("\\", "\\\\") + 'HOST_CON.db'