OWNER :=cogentdom
IMAGE_NAME :=stock-forecast-demo
VERSION :=v0.1
REPOSITORY :=fullstack-datascience
IMAGE_ID :=380443b0f0da
REGISTRY :=cogentdom
GITHUBTOKEN ?= $(shell echo $$GITHUBTOKEN)

default: 
	@echo 'Specify target'

new: build_new
git: login_git tag_git build_git publish_git
drhub: build_drhub publish_drhub

all: git drhub

# ------ Initial build ------
build_new: ## Build the container without caching
	docker build -t $(IMAGE_NAME):$(VERSION) .


# ------ Dockhub build ------
build_drhub: ## Build the container without caching
	docker build -t $(REGISTRY)/$(IMAGE_NAME):$(VERSION) .

# release_dh:  ## Make a release by building and publishing tagged image to Docker Trusted Registry (DTR)

publish_drhub: ## Publish image to DTR
	@echo 'publish $(REGISTRY)$(IMAGE_NAME):$(VERSION)'
	docker push $(REGISTRY)/$(IMAGE_NAME):$(VERSION)


# ------ Github build ------
login_git: ## Authenticate with GitHub Container Registry
	@echo "Logging in to GitHub Container Registry..."
	@echo $(GITHUBTOKEN) | docker login docker.pkg.github.com -u $(OWNER) --password-stdin

tag_git:
	docker tag $(IMAGE_ID) docker.pkg.github.com/$(OWNER)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION)

build_git: ## Build the container forrmated for githubs api
	docker build -t docker.pkg.github.com/$(OWNER)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION) .

# release_git: tag_git build_git publish_git ## Make a release by building and publishing tagged image to Docker Trusted Registry (DTR)

publish_git: ## Publish image to DTR
#	@echo 'publish $(REGISTRY)/$(IMAGE_NAME):$(VERSION)'
	docker push docker.pkg.github.com/$(OWNER)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION)
