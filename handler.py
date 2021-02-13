from bs4 import BeautifulSoup
import os
import urllib3
import json

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}


def lambda_handler(event, context):
    title = os.getenv('TITLE')
    url = os.getenv('URL')
    element_selector = os.getenv('ELEMENT_SELECTOR')
    expected_value = os.getenv('EXPECTED_VALUE')

    try:
        element_value = get_element_value(url, element_selector)

        if element_value != expected_value:
            message = "Expected value: %s, actual value: %s. Go to: %s" % (expected_value, element_value, url)
            print(message)
            send_notification_via_pushbullet(title, message)
        else:
            print("Element expected value: %s" % expected_value)
    except RuntimeError as e:
        send_notification_via_pushbullet("Error! %s" % title, "Exception: %s" % (str(e)))
        return ERROR_RESPONSE

    return OK_RESPONSE


def get_source(url):
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    print("Fetching source from: %s" % url)
    resp = http.request(
        "GET",
        "http://api.scrapestack.com/scrape?access_key=%s&url=%s" % (os.getenv("SCRAPER_API_ACCESS_TOKEN"), url)
    )

    if resp.status != 200:
        raise RuntimeError('Unable to get page source')

    return resp.data


def get_element_value(url, element_selector):
    page_source = get_source(url)
    print("Selecting element %s" % element_selector)
    soup = BeautifulSoup(page_source, "html.parser")
    element = soup.select(element_selector)

    if not element:
        raise RuntimeError('Unable to find element')

    return element[0].text


def send_notification_via_pushbullet(title, body):
    data_send = {"type": "note", "title": title, "body": body}
    print('Sending Notification')
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    resp = http.request(
        "POST",
        "https://api.pushbullet.com/v2/pushes",
        body=json.dumps(data_send),
        headers={'Authorization': 'Bearer ' + os.getenv("PUSHBULLET_ACCESS_TOKEN"), 'Content-Type': 'application/json'}
    )

    if resp.status != 200:
        raise Exception('Something went wrong sending notification')

    print('Notification sent')


# if __name__ == '__main__':
#     lambda_handler()
