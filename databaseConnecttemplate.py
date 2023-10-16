#blank connection string to be use with sqlAchemy this can be modified based on the requiremets for the database being connected to

#postGreSQL connection string
def get_connectionString():
    user = '' 
    password = ''
    host = '' 
    port = ''
    database = '' 
    return "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database)

    