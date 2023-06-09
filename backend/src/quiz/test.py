while len(alternatives) < 4:
		alt = Hit.query\
			.filter(
                # Finn artist med tilsvarande plassering på lista
				Hit.peak <= LEVELS[level]['peak'], 
				# Finn artist med like langvarig plassering på lista
				Hit.weeks >= LEVELS[level]['weeks'], 
				# Finn artist som var aktive i nærliggande tid
				Hit.year.in_(range(q.year-5,q.year+5)), 
				# Finn artist som ikkje allereie ligg i alternatives
				Hit.artist.not_in(alternatives), 
			).order_by(func.random()).limit(1).first()
		alternatives.append(alt.artist)