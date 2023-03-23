# Currency Exchange API
Test application for getting currency rate
## Install
Clone this repository to your local repository:<br/> 

```git clone https://github.com/vsevaq/currenccy_app.git```

First of all you have to install all dependencies.
Just write in your console:

```pip3 install -r requirements.txt```

Maybe you'll have to upgrade your pip.

Than you'll have to install postgres v-13+
Follow this link: https://www.postgresql.org/download/

Also you have to change your api_config.py vars to your local PostgreSQL configs: 

```pg_user, pg_password, pg_url, pg_database ```


## Run api server
To run REST api server open your terminal and type next command:

```python3.10 main.py```

## Api documentation

To check api endpoints and description for them put next url to your browser line:

```http://localhost:5000/docs```