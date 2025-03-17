from datetime import datetime, time, date

class DatesWorker:
    def __init__(self):
        self.currentDatetime = self.getCurrentDatetime()
        self.currentDate = self.getCurrentDate()
    
    def getCurrentDatetime(self):
        # Get current datetime
        current_datetime = datetime.now()

        # Convert to string
        datetime_string = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return datetime_string
    
    def getCurrentDate(self):
        # Get current date
        current_date = date.today()

        # Convert to string
        date_string = current_date.strftime('%Y-%m-%d')
        return date_string
    
    def getDates(self,date):
        #There can be two types of dates, one is a range and the other is a single date
        # 1. 01.01.2018 - 01.01.2019
        # 2. From Monday 01.01.2018
        #If there is a range, we need to split it and return both dates
        #If there is a single date and words, we need to return that date
        if " - " in date:
            dates =date.split(" - ")
            dates = self.changeDatesToRightFormat(dates)
            return {"startDate": dates[0], "endDate":dates[-1]}
        else:
            #we remove words from string
            dates = date.split(" ")
            dates = [dates[-1]]
            dates = self.changeDatesToRightFormat(dates)
            return {"startDate":dates[0], "endDate":""}
        
    def changeDatesToRightFormat(self, dates):
        #Tranforms dates from 01.01.2018 to 2018-01-01
        fixed_dates = []
        
        for date in dates:
            date = date.split(".")
            fixed_dates.append(date[2] + "-" + date[1] + "-" + date[0])

        return fixed_dates
    
    def compareDates(self, date2, end = True):
        #Compares two dates where date1 is current date and date2 is the date from the brochure
        #If end is True then we are dealing with end date, if False then we are dealing with start date
        #Because some brochures have only start date, we need to check if the current date is greater or equal
        date1 = datetime.strptime(self.currentDate, "%Y-%m-%d")
        date2 = datetime.strptime(date2, "%Y-%m-%d")
        
        if end:
            return date1 <= date2
        else:
            return date1 >= date2
        

