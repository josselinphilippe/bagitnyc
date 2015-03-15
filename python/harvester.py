import exceptions

from cartodb import CartoDBAPIKey, CartoDBException

from instagram.client import InstagramAPI


api_key = '700987471291d9c006a998b500f23de243f7388a'
cartodb_domain = 'jossphilippe'
cl = CartoDBAPIKey(api_key, cartodb_domain)


def insert_into_cartodb(sql_query):
    try:
       # your CartoDB account:
        print cl.sql(sql_query)
    except CartoDBException as e:
        print ("some error ocurred", e)


def get_max_id():
    return cl.sql('SELECT MAX(media_id) FROM instagram_media')['rows'][0]['max']


def Instagram_API(min_id=None):
    api = InstagramAPI(client_id='edf88a2a6fa94c9889e9800db8317f68', client_secret='73975e1a5b674c8e961568c463f3a8ec')
    bagitnyc_media = []

    # Get up to 200 media
    for page in api.tag_recent_media(tag_name='bagitnyc', as_generator=True,
                                     max_pages=10):
        # Open the page and push its contents onto bagitnyc_media
        bagitnyc_media += page[0]

    # If min_id passed, only return media that came after it.
    # Lambda is the same as defining a new function within the filter function. If min_id is passed in the API.tag_recent_media, retrieve all media with with greater id value (photos taken since oldest photo in api call) 
    
#    if min_id:
#        bagitnyc_media = filter(lambda m: m.id > min_id, bagitnyc_media)
    return bagitnyc_media


def create_sql_statement(x, y, link, media_credit, media_id, url, created_time):
    # Start with a basic INSERT statement
    # -> Don't forget to replace with your table name
    sql_query = 'INSERT INTO instagram_media (the_geom, link, media_credit, media_id, url, created_time) VALUES ('

    # Add our values to the statement, making sure that we wrap string values
    # in quotes
    # 4/8, EB: Fixed bug on next line that rounded x/y down to very low
    # precision
    sql_query = sql_query + "'SRID=4326; POINT (%f %f)', '%s', '%s', '%s', '%s', '%s'" % (x, y, link, media_credit, media_id, url, created_time)
    sql_query = sql_query + ')'
    return sql_query

 
if __name__ == '__main__':
    #
    # For each row in whatever is returned from get_data(), create an SQL
    # INSERT statement for that data, then insert it into CartoDB.
    #
    for media in Instagram_API(min_id=get_max_id()):
        try:
            # ONLY look at pieces of media with a location
            if media.location:
                sql_query = create_sql_statement(
                    media.location.point.longitude,
                    media.location.point.latitude,
                    media.images['standard_resolution'].url,
                    media.user.username,
                    media.id,
                    media.link,
                    media.created_time
                )
#                print(sql_query)

                # This is where you call insert_into_cartodb()
                insert_into_cartodb(sql_query)
        except exceptions.AttributeError:
            pass

if __name__ == '__main__':
    try:
     cl.sql('DELETE FROM instagram_media WHERE cartodb_id NOT IN (SELECT MIN(cartodb_id) FROM instagram_media GROUP BY url)')
    except CartoDBException as e:
        print ("some error ocurred", e)
