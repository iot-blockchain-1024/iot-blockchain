MYSQL_DATABASE_USER = 'iotplatform_yfge'
MYSQL_DATABASE_DB = 'iotplatform_yfge'
MYSQL_DATABASE_PASSWORD = 'izcP5Cc6F3TRfzsh'
MYSQL_DATABASE_HOST = 'iotplatform.yfgeek.com'


class Development(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}".format(MYSQL_DATABASE_USER, MYSQL_DATABASE_PASSWORD,
                                                               MYSQL_DATABASE_HOST, MYSQL_DATABASE_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Testing(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}".format(MYSQL_DATABASE_USER, MYSQL_DATABASE_PASSWORD,
                                                               MYSQL_DATABASE_HOST, MYSQL_DATABASE_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = True



class Production(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}".format(MYSQL_DATABASE_USER, MYSQL_DATABASE_PASSWORD,
                                                               MYSQL_DATABASE_HOST, MYSQL_DATABASE_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

