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
* [Maxime Hermez](https://github.com/MaxHermez)
* [Maximilien Monteil](https://github.com/MaxMonteil)
* [Waseem Elghali](https://github.com/Sauronsring)

## Getting Started

### Prerequisites

You will need to have a [Google Cloud Platform](https://cloud.google.com/) instance.

Make sure you also have [pipenv](https://pipenv.readthedocs.io) installed on your machine in order to easily set up the environment.

### Installing

```
git clone git@github.com:MaxMonteil/awe.git
cd awe
pipenv install

# to install the website dependencies
cd site
npm install
```

## Built With
