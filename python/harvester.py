import exceptions
from cartodb import CartoDBAPIKey, CartoDBException
from instagram.client import InstagramAPI

 # set variables for script
var_api_key = '700987471291d9c006a998b500f23de243f7388a'
var_cartodb_domain = 'jossphilippe'
var_client_id = 'edf88a2a6fa94c9889e9800db8317f68'
var_client_secret = '73975e1a5b674c8e961568c463f3a8ec'
var_tag_name = 'bagitnyc'
var_table_name = 'instagram_media'

# # your CartoDB account:
#var_api_key = 'your_api_key_here'
#var_cartodb_domain = 'your_username_here'
#var_client_id = 'your_client_id_here'
#var_client_secret = 'your_client_secret_here'
#var_tag_name = 'tag'
#var_table_name = 'tablename'




def insert_into_cartodb(sql_query):
    cl = CartoDBAPIKey(var_api_key, var_cartodb_domain)
    try:
       # your CartoDB account:
        print cl.sql(sql_query)
    except CartoDBException as e:
        print ("some error ocurred", e)


def Instagram_API():
    api = InstagramAPI(client_id= var_client_id, client_secret= var_client_secret)
    bagitnyc_media, pagination = api.tag_recent_media(150, 0, var_tag_name)
    return bagitnyc_media
    return pagination


def create_sql_statement(x, y, link, media_credit, media_id, url):
    # Start with a basic INSERT statement
    sql_query = 'INSERT INTO %s", var_table_name (the_geom, link, media_credit, media_id, url) VALUES ('

    # Add our values to the statement, making sure that we wrap string values
    # in quotes
    # 4/8, EB: Fixed bug on next line that rounded x/y down to very low
    # precision
    sql_query = sql_query + "'SRID=4326; POINT (%f %f)', '%s', '%s', '%s', '%s'" % (x, y, link, media_credit, media_id, url)
    sql_query = sql_query + ')'
    return sql_query



if __name__ == '__main__':
    #
    # For each row in whatever is returned from get_data(), create an SQL
    # INSERT statement for that data, then insert it into CartoDB.
    #
    for media in Instagram_API():
        try:
            # 4/8, EB: Added this check to ONLY look at pieces of media with a
            # location
            if media.location:
        
#                 4/8, EB: Changed this line to print lat and lng out
                print media.images['standard_resolution'].url, media.user.username, media.id, media.location.point.latitude, media.location.point.longitude, media.link


#                 4/8, EB: Added this line to print SQL statements for each
#                 piece of media
                print create_sql_statement(
                    media.location.point.longitude,
                    media.location.point.latitude,
                    media.images['standard_resolution'].url,
                    media.user.username,
                    media.id,
                    media.link

                
                sql_query = create_sql_statement(
                    media.location.point.longitude,
                    media.location.point.latitude,
                    media.images['standard_resolution'].url,
                    media.user.username,
                    media.id,
                    media.link
)
                print(sql_query)
                # This is where you call insert_into_cartodb()
                insert_into_cartodb(sql_query)
                    

                # This is where you could call insert_into_cartodb()
        except exceptions.AttributeError:
            pass
