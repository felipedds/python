import requests
from bs4 import BeautifulSoup
import smtplib
import email.message

def web_scraper_email():
    # Declare the variable that will be the body of the email
    body_email = ''

    # Dictionarie URL's
    urls = {'Market News All':'https://www.dailyfx.com/feeds/market-news',
            'Market News Forecasts':'https://www.dailyfx.com/feeds/forecasts',
            'Trading Strategies Technical Analysis':'https://www.dailyfx.com/feeds/technical-analysis',
            'Trading Strategies Sentiment':'https://www.dailyfx.com/feeds/sentiment'}

    for key, value in urls.items():
        # Request the URL
        request = requests.get(value)
        # Get the content of the page
        soup = BeautifulSoup(request.content)
        items = soup.find_all('item')
        for item in items:
            title = item.title.text
            description = item.description.text
            content = f'''<p>{title} \n{description}</p>'''
            body_email += content
            print(f'Title: \n{title} \nDescription: \n{description}\n')

        # Set up the set of information about the email
        msg = email.message.Message()
        msg['Subject'] = key
        msg['From'] = 'felipediasd@gmail.com'
        msg['To'] = 'felipe_dds@yahoo.com.br'
        password = 'n@tiruts8999'
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(body_email)

        smtp = smtplib.SMTP('smtp.gmail.com: 587')
        smtp.starttls()
        smtp.login(msg['From'], password)
        smtp.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Send email')

if __name__ == '__main__':
    web_scraper_email()
