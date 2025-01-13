build:
	docker build --progress=plain --network=host -t anirecs-image .

run:
	docker run --network=host --name anirecs-container anirecs-image

run-background:
	docker run -d -p 8000:8000 --name anirecs-container anirecs-image

remove-image:
	docker image rm anirecs-image

remove:
	docker remove anirecs-container

