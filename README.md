# Medcombo

  Es un website multifuncional especializada en el area farmaceutica en donde las empresas pueden publicar sus
  productos y servicios.

# Tecnologias usadas para este proyecto

  Django 2.2.6, Python >3.5.3, Bootstrap 4.3.1 y jquery 3.3.1

# Instalación

prerequisitos

* pip:

  instalamos pip3 metodo get pip

  sudo apt-get install curl

  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

  sudo python3 get-pip.py

* virtualenv (opcional):

  Instalar virtualenv

  sudo apt-get install python-virtualenv virtualenv

  Comando para ver ruta de nuestro interprete python:

  which python3

  Comando para crear entorno virtual:

  virtualenv nombre_de_mi_entorno -p /usr/bin/python3

  Comando para activar el entorno:

  source nombre_de_mi_entorno/bin/activate

  Comando para desactivar el entorno:

  deactivate

1.Clonar repositorio.

    git clone https://github.com/jonathanaraul/Medcombo.git

2.Entrar a la carpeta Medcombo.

    cd Medcombo

3. Instalar dependencias con pip. (Si estas usando entorno virtual recuerda activarlo)

    pip install -r requirements/local.txt

4.Realizar las migraciones

    python manage.py makemigrations

    o hacer las migraciones por separado en caso de que no falle el comando 
    
    python manage.py makemigrations cities_light
    python manage.py makemigrations location
    python manage.py makemigrations company
    python manage.py makemigrations usercustom
    python manage.py makemigrations product
    python manage.py makemigrations contacts
    python manage.py makemigrations catalogue
    python manage.py makemigrations call
    python manage.py makemigrations contact
    python manage.py makemigrations dashboard_admin
    python manage.py makemigrations opportunity
    python manage.py makemigrations task
    python manage.py makemigrations post
    python manage.py makemigrations job
    python manage.py makemigrations economic

    y por ultimo crear la base de datos

    python manage.py migrate

5.Correr el proyecto:

    python managy.py collectstatic

    python managy.py compress --force

    python manage.py cities_light --force-all
    
    python manage.py runserver

Cargar datos de prueba (Opcional):
    
* En local: 

    python manage.py loaddata medcombo/configuration/location/data/cities_light_country.json
    python manage.py loaddata medcombo/configuration/location/data/cities_light_region.json
    python manage.py loaddata medcombo/configuration/location/data/cities_light_city.json
    python manage.py loaddata medcombo/configuration/company/data/invoicingtitle.json
    python manage.py loaddata medcombo/configuration/company/data/company_medcombo.json
    python manage.py loaddata medcombo/configuration/usercustom/data/user_admin_test.json
    python manage.py loaddata medcombo/crm/dashboard_admin/data/language_campaign.json
    python manage.py loaddata medcombo/myweb/company/data/languagemodel.json
    python manage.py loaddata medcombo/myweb/job/data/contracts.json
    python manage.py loaddata medcombo/myweb/job/data/workdays.json
    python manage.py loaddata medcombo/configuration/usercustom/data/work.json
    python manage.py loaddata medcombo/crm/data/state.json
    python manage.py loaddata medcombo/crm/opportunity/data/contactedby.json
    python manage.py loaddata medcombo/crm/task/data/priority.json
    python manage.py loaddata medcombo/crm/task/data/calltasks.json
    python manage.py loaddata medcombo/crm/dashboard_admin/data/campaigns.json
    python manage.py loaddata medcombo/crm/dashboard_admin/data/banners.json
    python manage.py loaddata medcombo/crm/dashboard_admin/data/banners_index.json
    python manage.py loaddata medcombo/crm/dashboard_admin/data/banners_user.json
    python manage.py loaddata medcombo/product/data/policyprivacy.json
    python manage.py loaddata medcombo/product/data/area.json
    python manage.py loaddata medcombo/product/data/category.json
    python manage.py loaddata medcombo/product/data/subcategory.json
    python manage.py loaddata medcombo/product/data/keyword.json 


* En servidor de pruebas:

    python manage.py loaddata medcombo/configuration/location/data/cities_light_country.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/configuration/location/data/cities_light_region.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/configuration/location/data/cities_light_city.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/configuration/company/data/invoicingtitle.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/configuration/company/data/company_medcombo.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/configuration/usercustom/data/user_admin_test.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/crm/dashboard_admin/data/language_campaign.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/myweb/company/data/languagemodel.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/crm/data/state.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/crm/opportunity/data/contactedby.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/crm/task/data/priority.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/crm/task/data/calltasks.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/myweb/job/data/contracts.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/myweb/job/data/workdays.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/configuration/usercustom/data/work.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/crm/dashboard_admin/data/campaigns.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/crm/dashboard_admin/data/banners.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/crm/dashboard_admin/data/banners_index.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/crm/dashboard_admin/data/banners_user.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/product/data/policyprivacy.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/product/data/area.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/product/data/category.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/product/data/subcategory.json --settings=medcombo.settings.test
    python manage.py loaddata medcombo/product/data/keyword.json --settings=medcombo.settings.test

# Usar con docker

sudo docker-compose -f docker-compose-local.yml build
sudo docker-compose -f docker-compose-local.yml up
sudo docker-compose -f docker-compose-local.yml run web python manage.py run_chat_server --settings=medcombo.settings.docker_local
