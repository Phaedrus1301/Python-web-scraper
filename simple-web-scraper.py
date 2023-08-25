#library imports necessary for this code
import requests
from bs4 import BeautifulSoup
import pandas as pd

#in base url you can put the target base URL. ex - "https://www.amazon.com/"
baseurl = ""
#headers so that the receiving browser sees that all the fetch data query is from a webbrowser instead of python
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

productlinks = []

#for loop's range = number of pages on product page.
#for ex. "https://www.sephora.com/shop/makeup-cosmetics" this page has 2673 products and each page shows 60 products,
#so we can just do the math and assume there will be about 45 pages. so the range of for loop in this case will be (1,45)

for x in range(1,6):
    #example of sephora continued, you can now replace x with page number in the below url and hence it will open up all the pages
    k = requests.get('https://www.sephora.com/shop/makeup-cosmetics?currentPage={}'.format(x)).text

    #here we use beautifulsoup4 to parse the html page and then command it to find certain elements, this can be done with .find() command
    #you can parse in different values like div, span or even h1 etc. second part of find_all grabs all of text inside of mentioned div
    soup=BeautifulSoup(k,'html.parser')
    productlist = soup.find("div", {"class":"main-products product-grid"}).find_all("div",{"class":"caption"})
    #print(productlist)
    #we can just print and check if we are getting the correct value or not and then make modifications accordingly before continuing.

    #here we are sorting the text, bascially instead of going again and again to browser link, now that we have whole bunch of divs from previous fetch, 
    #we just need to filter it again to get specific data, like the link to their product page itself.
    for product in productlist:
        link = product.find("div", {"class":"name"}).find("a").get('href')        
        productlinks.append(link)

    #print(productlinks)
    #once again we only print productlinks, these small print steps allow us to locate any errors at the same time and then move one once it is solved.


productsku = []
productname = []
productprice = []

#loops all the link we found from main products page and then gets required information out of them.
for link in productlinks:

    #once again here, we parse the link and the html parser so we can look more in depth into single products page and then fetch even more details as we need them.
    f = requests.get(link, headers=headers).text
    buh = BeautifulSoup(f, 'html.parser')

    #trying out to find specific divs and more parts, this should be modified by you depending on your target website, same goes for above for-loop we used to get links as well.
    try:
        name = buh.find("div", {"class":"title page-title"}).get_text()
        price = buh.find("div", {"class":["product-price-new","product-price"]}).get_text().replace("₹","")
        model = buh.find("li",{"class":"product-model"}).find("span").get_text()
    except:
        model = "Not found"
        price = "Not found"
        name = 'Not found'

    #here we are appending all the data we found into lists, so we can use it later.
    productname.append(name)
    productprice.append(price)
    productsku.append(model)

#now we have created a dictionary of all the information we have collected
cabinets = {"Product SKU":productsku, "Price":productprice, "Name":productname}
#print(cabinets)
#after trying it out with a print to be sure it has no errors, we will now add it into dataframe using pandas
df = pd.DataFrame(cabinets)

#once the dataframe is set, we can then create output excel file for whatever reason we need it.
#run this first time with if_sheet_exists='new' to create and enter data in new excel sheet, then change it to if_sheet_exists='replace' for all the reruns so it will overwrite existing worksheet.
with pd.ExcelWriter("C:\\Users\\User\\Downloads\\your-file-name\\output-data.xlsx", mode="a", engine= 'openpyxl', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='output-for-perfumes', index=False)
#you can use this as adviced, it will create multiple sheets within a single excel output file, i chose this way because i need it for some reason, there are other ways to do the same.