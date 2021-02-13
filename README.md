# Lambda Scraper

Periodically scrapes a website and sends a notification via Pushbullet if the selected element is different to the expected value.

Useful for monitoring a change in stock level on an E-commerce website.

Uses:
- Python 3.8
- AWS Lambda
- Serverless framework
- Serverless plugin serverless-python-requirements
- [Scrapestack.com](https://scrapestack.com/) for scraping
- [Pushbullet](https://www.pushbullet.com/) for notifications

## Setup

1\. Create Python virtualenv
```
python3 -m venv .venv
```

2\. Copy environment vars file and set variables
```
cp serverless.env.yml.dist serverless.env.yml
```

3\. Deploy Lambda function with Serverless
```
serverless deploy
```

