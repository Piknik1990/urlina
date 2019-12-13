# URLINA

Basic testing of sites. Easy and Pipeline-ready!

## What is it?

URLINA is a easy software for checking HTTP-status codes of your site. It's really best additinal for your Pipeline! And not one corner of the site will be forgotten!

### It's easy work

You need to create a check-list of URL with expected status сode.  Then start URLINA and she will check and compare real and expected status code for any URL. If they is identical - APLINA will return the "OK" status of check. If not - will return the "FAIL" status, unsuccess status code of run command, Fail your Pipeline, arrange global darkening, will erupt all volcanoes on earth, destroy humanity and put out the sun (the last 4 features are still in development).

### It's easy starting

#### Modules

Install python-modules

Example for Fedora:

```shell
# Python2
dnf install python2-pyyaml python2-requests -y

# Python3
dnf install python3-pyyaml python3-requests -y
```

#### First

Create a yaml-file with follow content:

`test.yaml`

```yaml
urls:
  - url: https://github.com
  - url: https://github.com/nowhere/nowhere
    code: 404
  - url: https://github.com/settings/profile
    code: 422
    method: POST
```

Where is:

* **url** (req) - URL for testing.
* **code** - the comparing code status (default: 200)
* **method** - setting a requiest method (default: GET)

#### Second

Start URLINE:

`./urline.py test.yaml`

or

`./urline3.py test.yaml`

Options:

* **-h** Get help
* **-s** Skip not matching a status codes
* **-c** Check SSL validation
* **-r** Add "Rederer" header as testing URL
* **-d** Debug mode.
* **-txx** Timeout of requests. Default: 10 (sec), min: 1 (sec), max: 3600 (sec)

#### Last

See result!

```shell
$ ./urlina.py test.yaml 
Checking...
Status	Method	Code	Comparing code	Address
OK	    GET	    200	  200		          https://github.com
OK	    GET	    404	  404		          https://github.com/nowhere/nowhere
OK	    POST	  422	  422		          https://github.com/settings/profile
Done.
```

### Docker

#### Running

You can to run it in docker container. It's easy too - you need to volume your yaml-file to docker-container and set his into end of commandline.

```shell
# Python2
docker run -v $(pwd)/test.yaml:/usr/src/app/test.yaml piknik1990/urlina:1.0-p2 test.yaml 

# Python3
docker run -v $(pwd)/test.yaml:/usr/src/app/test.yaml piknik1990/urlina:1.0-p3 test.yaml 
```

Result:

```shell
$ docker run -v $(pwd)/test.yaml:/usr/src/app/test.yaml piknik1990/urlina:latest test.yaml 
Checking...
Status  Method	Code	Comparing code	Address
OK	    GET	    200	  200		          https://github.com
OK	    GET	    404	  404		          https://github.com/nowhere/nowhere
OK	    POST	  422	  422		          https://github.com/settings/profile
Done.
```

#### Building

You can to build your new docker-image

```shell
# Python2
cp urlina.py docker/python2/
docker build -t piknik1990/urlina:1.0-p2 docker/python2/.
rm -f docker/python2/urlina.py
docker push piknik1990/urlina:1.0-p2

# Python3
cp urlina3.py docker/python3/
docker build -t piknik1990/urlina:1.0-p3 docker/python3/.
rm -f docker/python3/urlina3.py
docker push piknik1990/urlina:1.0-p3
docker tag piknik1990/urlina:1.0-p3 piknik1990/urlina:latest
docker push piknik1990/urlina:latest
```

## Authors

* **Malinin Ivan**
* **Nifanin Konstantin**

## Links

* [Source code](https://github.com/Piknik1990/urlina)
