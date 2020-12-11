def search_torr(start_date, end_date): #called in views.search
	cmd = f'''
	SELECT *
	FROM
		(SELECT torr_id, name, DATE(rarbg_added) rarbg_added, size, size_units, 
			n_seed, n_leech, rarbg_url, infohash, imdb_id, title, n_keywords
		FROM torrents.torrent_full tf) tf_date
	WHERE rarbg_added >= DATE("{start_date}")
	AND rarbg_added <= DATE("{end_date}")
	ORDER BY rarbg_added DESC
	'''
	return cmd