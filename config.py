import os
basedir = os.path.abspath(os.path.dirname(__file__))

#necessary so that our server does not need https
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Config(object):
    # good practice to take enviroment variables and add a default one in case it fails
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # database config # 
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False

    