import requests
from bs4 import BeautifulSoup
import pandas as pd

# Make a GET request to the website you want to scrape
# url = "https://www.sigmaaldrich.com/BE/en/product/sial/phr1009"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
url = 'https://www.sigmaaldrich.com/ES/en/products/analytical-chemistry/reference-materials/pharma-secondary-standards?country=ES&language=en&cmsRoute=products&cmsRoute=analytical-chemistry&cmsRoute=reference-materials&cmsRoute=pharma-secondary-standards&page=1&facets=facet_web_special_grade%3Apharmaceutical+secondary+standard'
response = requests.get(url, headers=headers)
# print(response)

product_datas = {
    'Product No.': [],
    'Description': [],
    'CAS': [],
    'Package Size': [],
    'Price(Euro)': [],
    'BP Traceability': [],
    'Ph.Eur Traceability': [],
    'USP Traceability': []
    
}

def get_product_data(product_url):
    product_data = {
        'no': '-',
        'description': '-',
        'CAS': '-',
        'pack_size': '-',
        'price': '-',
        'BP_trace': '-',
        'PH_EUR_trace': '-',
        'US_trace': '-'
    }
    trace_text = set()
    access_url = "https://www.sigmaaldrich.com" + product_url
    # access_url = "https://www.sigmaaldrich.com/BE/en/product/sial/phr1084"
    response = requests.get(access_url, headers=headers)
    sop = BeautifulSoup(response.content, 'html.parser')
    # print(sop.find(id="product-number"))
    element = sop.find_all(class_=lambda x: x and "MuiTypography-body2" in x)
    table = sop.find('table')
    print("table=========", table)
    element_price = sop.find_all(class_=lambda x: x and "MuiTableCell-root" in x)
    print(element_price)
    span_elements = element[2].find_all('span')
    for span in span_elements:
        trace_text.add(span.text)
    # print(span_elements)
    # print(trace_text)
    product_data['no'] = sop.find(id="product-number").get_text()
    product_data['description'] = sop.find(id="product-name").get_text()
    product_data['CAS'] = sop.find(id=lambda x: x and "-alias-link" in x).get_text()
    product_data['pack_size'] = sop.find(id=lambda x: x and "-alias-link" in x).get_text()
    product_data['price'] = sop.find(id=lambda x: x and "-alias-link" in x).get_text()
    for text in trace_text:
        if (not text.find("traceable to BP")):
            if product_data['BP_trace'] != '-':
                product_data['BP_trace'] = product_data['BP_trace'] + "/" + text.replace("traceable to BP", "").replace(" ", "")
            else:
                product_data['BP_trace'] = text.replace("traceable to BP", "").replace(" ", "")
        elif (not text.find("traceable to Ph. Eur.")):
            if product_data['PH_EUR_trace'] != '-':
                product_data['PH_EUR_trace'] = product_data['PH_EUR_trace'] + "/" + text.replace("traceable to Ph. Eur.", "").replace(" ", "")
            else:
                product_data['PH_EUR_trace'] = text.replace("traceable to Ph. Eur.", "").replace(" ", "")
        elif (not text.find("traceable to USP")):
            if product_data['US_trace'] != '-':
                product_data['US_trace'] = product_data['US_trace'] + "/" + text.replace("traceable to USP", "").replace(" ", "")
            else:
                product_data['US_trace'] = text.replace("traceable to USP", "").replace(" ", "")
    save_data(product_data)
    print(product_data)

def save_data(data):
    product_datas['Product No.'].append(data['no'])
    product_datas['Description'].append(data['description'])
    product_datas['CAS'].append(data['CAS'])
    product_datas['Package Size'].append(data['pack_size'])
    product_datas['Price(Euro)'].append(data['price'])
    product_datas['BP Traceability'].append(data['BP_trace'])
    product_datas['Ph.Eur Traceability'].append(data['PH_EUR_trace'])
    product_datas['USP Traceability'].append(data['US_trace'])

# Check the status code of the response
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find(class_="jss122")
    result_a = result.find_all('a')
    result_href = {tag.get('href') for tag in result_a}

    # print(result_href)

    for product_url in result_href:
        get_product_data(product_url)

    # get_product_data("example.com")
    
    print(product_datas)
    df = pd.DataFrame(product_datas)
    sorted_df = df.sort_values('Product No.')
    sorted_df.to_excel('result.xlsx', index=False)
    # Find the elements you want to extract data from
    # For example, to extract all the links on the page:
else:
    print('Error: Could not retrieve data from website')



