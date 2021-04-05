# Whatsapp Api Service
Unofficial whatsapp api for bussiness with integrated user panel interface
---

#### Story :
this project was inspired from chat-api.com apiwha.com which is a service provider of unofficial whatsapp api for bussiness.

#### Required :
1. Docker compose

#### Install : 
```bash
# clone this repo
git clone https://github.com/simiprambos/django-whatsapp.git
cd django-whatsapp

# build docker image
docker-compose build .

# run
docker-compose up -d

# create admin account
docker-compose exec backend python3 manage.py createsuperuser
```

#### Usage :
this project is actually to complete my assignment as a freelancer, therefore for now I can't provide documentation here, if this can be useful for you please contact me and let's discuss :D
