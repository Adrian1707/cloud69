# Cloud69
An AWS infrastructure automation tool using Python / Django and AWS Cloud Formation Templates.

The idea is to abstract away the infrastructure provisioning for a standard Rails application. Provide a Github link,
some additional parameters like how many servers you want and hit "Create". It's often too fiddly to get something online without going 
through a managed PaaS like Elastic Beanstalk or Heroku, so this service provides a simple wrapper to AWS services


## Install

```
Ensure you have Docker and Docker Compose installed
git clone https://github.com/Adrian1707/cloud69
cd cloud69
docker-compose build
docker-compose up
visit localhost:8000/stacks
```
## Improvements / Work in Progress

- Don't hardcode VPC & subnets in the CF Template
- Allow multiple database adapters like Postgres, SQLite etc
- AWS user authentication / omniauth 
- Serverless / lambda automation feature
