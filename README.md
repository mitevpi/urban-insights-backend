# Urban Insights Backend

Backend for Urban Insights App.

[![Generic badge](https://img.shields.io/badge/Deployment-Heroku-green.svg)](https://urban-insights-api.herokuapp.com)

## Purpose

The Python backend houses the business logic for modle parsing, analysis, and geometry operations which are fed back into the frontend for realtime visualization with AR/VR.

## Developing and Deploying

### Develop

To develop the application locally, type `flask run` into the root directory of this repository. You can test methods locally with Postman using this configuration.

### Auto-Deploy to Heroku

Deployments happen automatically from the `deploy` branch of this repository. Once the `deploy` branch sees comitted changes, Heroku will rebuild the deployment at [this link](https://urban-insights-api.herokuapp.com). Once you're ready to deploy the changes from your local branch, just make a merge request into `deploy` and the build will happen automatically.

## Endpoints

**GET /cutObj**

> **Takes** Nothing yet
> **Returns** An OBJ model serialized to JSON.

**GET /getSunVector**

> **Takes** Body of data with the follwing param headers:
```json
{
    "address": "ib schonbergs alle 2 valby",
    "month": 6,
    "day": 21,
    "hour": 12
}
```
> **Returns** A string representation of the Sun Vector.

![api](assets/api.png)