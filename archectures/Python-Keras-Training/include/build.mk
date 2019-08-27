define PROJECT_HELP_MSG
Usage:
    make help                  show this message
    make build                 make image
    make push					push image
endef
export PROJECT_HELP_MSG

help:
	echo "$$PROJECT_HELP_MSG" | less

build:
	docker build -t $(image) $(dockerpath)

push:
	docker push $(image)


.PHONY: help build push
