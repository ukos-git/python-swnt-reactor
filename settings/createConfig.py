import ConfigParser
config = ConfigParser.RawConfigParser()

config.add_section('Database')
config.set('Database', 'dbUser', 'matthias')
config.set('Database', 'dbPass', 'myPassword')
config.set('Database', 'dbHost', '127.0.0.1')
config.set('Database', 'dbName', 'cvd')
config.add_section('Server')
config.set('Server', 'servername', 'atlas')
with open('settings.cfg', 'wb') as configfile:
    config.write(configfile)
