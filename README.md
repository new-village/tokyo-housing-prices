# Tokyo Housing Prices
This project is a REST API application that estimates housing prices in Tokyo.

## How to use
#### Execute application on local
1. Set environment variables by local.sh
```bash:
$ cd tokyo-housing-prices
$ cp init.sh local.sh
$ vim local.sh
$ source local.sh
```
  
2. Run Python script  
```bash:
$ cd tokyo-housing-prices
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install --upgrade setuptools
$ pip install -r requirements.txt
$ python main.py
```
  
#### Execute application on Azure Container Registry
1. Set environment variables  
```bash:
$ cd tokyo-housing-prices
$ cp init.sh local.sh
$ vim local.sh
$ source local.sh
```
  
2. Build Docker image & test run on local docker environment  
if your execution is finished successful, you can see new records in cosmos-db.
```
$ cd tokyo-housing-prices
$ docker build -t tokyo-housing-prices .
$ docker run --rm -e ${ACCOUNT_URI} -e ${ACCOUNT_KEY} -it tokyo-housing-prices
```

3. Push Image to Azure Container Registry
You can see pushed contaier image on Azure Container Registry > Repository after below commands.
```
$ docker login -u ${USERNAME} -p ${PASSWORD} ${REGISTRY}.azurecr.io
$ docker tag tokyo-housing-prices ${REGISTRY}.azurecr.io/tokyo-housing-prices
$ docker push ${REGISTRY}.azurecr.io/tokyo-housing-prices
```

4. Deploy Web Application
Select Repository > tokyo-housing-prices > latest and select `deploy webapps`  
You can see deployed application in `App Service` page.

5. Set Environment Variables
Select `App Service` > Configuration > New Application Setting.  
Then you have to set ACCOUNT_URI/ACCOUNT_KEY environment variables and Save configuration.
  
