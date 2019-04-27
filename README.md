# AWE

![AWE Logo](../assets/awe_logo.png "The AWE Logo")

The Accessibility Web Engine aims to make the web more accessible by following WACG 2.0 standard.

## Table of Contents

* [About This Project](#about-this-project)
* [The Team](#the-team)
* [Getting Started](#getting-started)
	* [Prerequisites](#prerequisites)
	* [Installing](#installing)
* [API Functions](#api-functions)
* [Deployment](#deployment)
* [Built With](#built-with)

## About This Project

Although the internet is now over 30 years old, it is still incredibly difficult for some people to navigate. Today with the huge amount of media content available, and with an ever increasing number connected people, it is more important than ever that a strong effort is made to create a more accessible internet.

This project aims to make the internet more accessible through our Accessibility Web Engine API which works by taking the URL of a page, scanning it, and returning a version that reaches or surpassed the WCAG 2.0 AA guideline level.

![API Structure](../assets/api_structure.png "The AWE API's structure")

## The Team

* [Hussein Murtada](https://github.com/husseinmur)
* [Maria Daou](https://github.com/mariadaou)
* [Marina Kayrouz](https://github.com/MarinaKeyrouz)
* [Maxim Hermez](https://github.com/MaxHermez)
* [Maximilien Monteil](https://github.com/MaxMonteil)
* [Waseem Elghali](https://github.com/Sauronsring)

## Getting Started

### Prerequisites

Have [pipenv](https://pipenv.readthedocs.io) installed on your machine in order to easily set up the environment.

You will also need to have Node 10.13+ installed in order to be able to run lighthouse.

### Installing

```
git clone git@github.com:MaxMonteil/awe.git && cd awe
cp env .env && echo "ROOT_DIR=$PWD" >> .env
pipenv install
npm install -g lighthouse
pipenv run pyppeteer-install
```

The first line clones the project to your machine and moves you into the folder.

The second line will create the environment variables file specific to your setup using the `env` file as a template. The part after the `&&` will add the `ROOT_DIR` variable to the environment which is the absolute path to the awe directory.

*If you are on Windows this line might not work, just rename the *`env`* file to *`.env`* and add a line like this 'ROOT_DIR=\Path\to\the\awe\folder'*

The third line runs pipenv which will read the Pipfile and create the python virtual environment.

Finally npm will install lighthouse.

**The last line is optional.**
Run it if you want to install Google Chrome for the project right now, otherwise pyppeteer will do it itself the first time it is run.


Next create a copy of the `env` file called `.env` (note the dot) and add in the absolute path to the root directory of awe.

ex: `/home/<username/awe`

## Built With

* Python
* Google Lighthouse
