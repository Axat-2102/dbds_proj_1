#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/dbds_proj_1')

from flaskapp import app as application