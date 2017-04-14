import os

os.environ['app_key'] = 'e9541829a44b426a81ccb828865424f2'
os.environ['app_secret'] = '168cb12ba3b54b069b863b09b6a00bc1'
os.environ['houdini_server'] = 'http://192.168.33.15'

# Emails
os.environ['EMAIL_USE_TLS'] = str(True)
os.environ['EMAIL_HOST'] = 'smtp.gmail.com'
os.environ['EMAIL_PORT'] = str(587)
# TODO: set an email up for activation emails
os.environ['EMAIL_HOST_USER'] = 'reports@thecorp.org'
os.environ['EMAIL_HOST_PASSWORD'] = 'S88JDnDyba6hC5qHXVQ2'

os.environ['BASE_URL'] = 'http://localhost:8080'
