from bs4 import BeautifulSoup
from jsonifyData import JsonifyData
from datesWorker import DatesWorker
import requests

class Parser:
    def __init__(self, url):
        self.base_url = self.getBaseUrl(url)
        self.soup = self.getWebsiteHtml(url)
        self.links = []
        
        self.finalData = []
        
        self.dateWorker = DatesWorker()
        
        
        self.getAllLinks()
        self.getDataFromBrochure()
        
        self.jsonify = JsonifyData()
        self.jsonify.writeDataToJson(self.finalData)
        
    def getWebsiteHtml(self,url):
        page = requests.get(url)
        html = page.content
        return BeautifulSoup(html, "html.parser")     
        
    def getBaseUrl(self, url):
        splittedUrl = url.split("/")
        return splittedUrl[0] + "//" + splittedUrl[2]
        
    def getAllLinks(self):
        linksWrapper = self.soup.find("ul", {"id":"left-category-shops"})
        for i in linksWrapper.find_all("a"):
            self.links.append(self.base_url + i["href"])
    
            
    def getDataFromBrochure(self):
        for i in self.links[0:5]:
            html = self.getWebsiteHtml(i) 
            
            brand = html.find("div", {"class":"page-poster produkt-poster text-center"}) 
            brand_name = brand.find("h1").get_text().split()[0] or "BrandMissing"         
            data={}

            
            pageBody = html.find("div", {"class":"page-body"})
            letaky = pageBody.find("div", {"class":"letaky-grid"})
            brochures = letaky.find_all("div", {"class":"brochure-thumb"})
            for i in brochures:
                data.clear()
                data["brand"] = brand_name
                data["parsed_time"] = self.dateWorker.currentDatetime
                
                if i.find("img").has_attr("src"):
                    img= i.find("img")["src"] or ""
                else:
                    img = i.find("img")["data-src"] or ""
                    
                content = i.find("div",{"class":"letak-description"})
                title = content.find("strong").get_text() or "Brochure"
                
                data["title"] = title
                data["thumbnail"] = img
                
                grid_item = i.find_all("p", {"class":"grid-item-content"})
                
                date = grid_item[1].find("small").get_text() or ""
                dates = self.dateWorker.getDates(date)
                

                if dates["endDate"] == "":
                    data["valid_from"] = dates["startDate"]
                    data["valid_to"] = "-"
                    self.finalData.append(data)
                elif self.dateWorker.compareDates(dates["endDate"]):
                    data["valid_from"] = dates["startDate"]
                    data["valid_to"] = dates["endDate"]
                    self.finalData.append(data)
                else: 
                    print("Brochure is outdated", data)
                    continue

                
                
            
