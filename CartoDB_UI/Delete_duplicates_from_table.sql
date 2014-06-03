
SELECT * FROM instagram_media WHERE cartodb_id NOT IN (SELECT MIN(cartodb_id) _
	FROM instagram_media GROUP BY url)  