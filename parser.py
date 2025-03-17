from bs4 import BeautifulSoup
from jsonifyData import JsonifyData
from datesWorker import DatesWorker
import requests

class Parser:
    def __init__(self, url):
        #initialize parser with url and soup object
        
        self.base_url = self.getBaseUrl(url)
        self.soup = self.getWebsiteHtml(url)
        self.links = []
        
        self.finalData = []
        
        #get access to time manager      
        self.dateWorker = DatesWorker()
        
        
    def getWebsiteHtml(self,url):
        # Fetch the HTML content of the webpage
        page = requests.get(url)
        html = page.content
        # Parse the HTML content using BeautifulSoup
        return BeautifulSoup(html, "html.parser")     
        
    def getBaseUrl(self, url):
        # Extract the base URL from the given URL
        # Example: https://www.example.com/new -> https://www.example.com
        splittedUrl = url.split("/")
        return splittedUrl[0] + "//" + splittedUrl[2]
        
    def getAllLinks(self):
        # Find all relevant links on the webpage

        linksWrapper = self.soup.find("ul", {"id":"left-category-shops"})
        for i in linksWrapper.find_all("a"):
            self.links.append(self.base_url + i["href"])
             
    def getDataFromBrochure(self):
        # Process each link to extract data from brochures
        for link in self.links:
            html = self.getWebsiteHtml(link) 
            
            # Extract the shop name

            shop = html.find("div", {"class":"page-poster produkt-poster text-center"}) 
            shop_name = shop.find("h1").get_text().split()[0] or "BrandMissing"         

            #get access to all comapnies brochures
            pageBody = html.find("div", {"class":"page-body"})
            letaky = pageBody.find("div", {"class":"letaky-grid"})
            brochures = letaky.find_all("div", {"class":"brochure-thumb"})
            
            for i in brochures:
                data={}

                #extract the image of brochure
                if i.find("img").has_attr("src"):
                    img= i.find("img")["src"] or ""
                else:
                    img = i.find("img")["data-src"] or ""
                    
                content = i.find("div",{"class":"letak-description"})
                title = content.find("strong").get_text() or "Brochure"
                
                data["title"] = title
                data["thumbnail"] = img
                data["shop_name"] = shop_name                
                
                #extract the date information of brochure
                grid_item = i.find_all("p", {"class":"grid-item-content"})
                
                date = grid_item[1].find("small").get_text() or ""
                dates = self.dateWorker.getDates(date)

                #check if the date is valid
                #if the date is valid, add the data to finalData
                if dates["endDate"] != "":
                    if self.dateWorker.compareDates(dates["endDate"]):
                        data["valid_from"] = dates["startDate"]
                        data["valid_to"] = dates["endDate"]
                        data["parsed_time"] = self.dateWorker.currentDatetime

                        self.finalData.append(data)     
                else:
                    if self.dateWorker.compareDates(dates["startDate"], False):
                        data["valid_from"] = dates["startDate"]
                        data["valid_to"] = "-"
                        data["parsed_time"] = self.dateWorker.currentDatetime
                        self.finalData.append(data)

    def mainAction(self):
        # Main action to get all links and data from brochures, and write to JSON
        self.getAllLinks()
        self.getDataFromBrochure()
        
        self.jsonify = JsonifyData()
        self.jsonify.writeDataToJson(self.finalData)
