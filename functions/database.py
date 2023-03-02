from django.db import connections

def status():
   try:
      # Use the 'default' database connection
      connection = connections['default']
      # Try to execute a simple query
      with connection.cursor() as cursor:
         cursor.execute('SELECT 1')
         cursor.fetchone()
      return 'The database is online. ✅'
   except:
      return 'The database is offline. ⚠️'
