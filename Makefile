run:
	docker-compose up -d

stop:
	docker-compose down

build:
	docker-compose build

shell:
	docker-compose exec -it spark-container /bin/bash

import_data:
	docker-compose exec spark-container python /app/import_data.py