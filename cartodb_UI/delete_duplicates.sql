#This is the necessary table cleanup statement to be included in the harvester.py script for a CRON job

#def delete_duplicates()
#    delete = """DELETE FROM  % var_table_name WHERE cartodb_id NOT IN 
#    (
#      SELECT MAX(cartodb_id) FROM var_table_name
#      GROUP BY media_id
#      )"""
#    return sql_query
