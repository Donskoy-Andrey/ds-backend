run:
	docker-compose up -d

stop-all-containers:
	docker stop $$(docker ps -a -q)

post_existed_image_9965:
	curl -X POST http://127.0.0.1:8080/read_plate_number \
	  -d "image_id=9965"

post_existed_image_10022:
	curl -X POST http://127.0.0.1:8080/read_plate_number \
	  -d "image_id=10022"

post_not_existed_image:
	curl -X POST http://127.0.0.1:8080/read_plate_number \
	  -d "image_id=992"

post_images_1:
	curl -X POST http://127.0.0.1:8080/read_plate_numbers \
	  -d "image_ids=9965,10022"

post_images_2:
	curl -X POST http://127.0.0.1:8080/read_plate_numbers \
	  -d "image_ids=9965,10023"

post_incorrect_input:
	curl -X POST http://127.0.0.1:8080/read_plate_numbers \
	  -d "image_ids=9965;10023"
