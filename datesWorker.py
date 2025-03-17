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
        if " - " in date:
            dates =date.split(" - ")
            dates = self.changeDatesToRightFormat(dates)
            return {"startDate": dates[0], "endDate":dates[-1]}
        else:
            dates = date.split(" ")
            dates = [dates[-1]]
            dates = self.changeDatesToRightFormat(dates)
            return {"startDate":dates[0], "endDate":""}
        
    def changeDatesToRightFormat(self, dates):
        fixed_dates = []
        
        for date in dates:
            date = date.split(".")
            try:
                fixed_dates.append(date[2] + "-" + date[1] + "-" + date[0])
            except:
                pass
        return fixed_dates
    
    def compareDates(self, date2):
        date1 = datetime.strptime(self.currentDate, "%Y-%m-%d")
        date2 = datetime.strptime(date2, "%Y-%m-%d")
        
        #print(date1, date2, date1 <= date2)
        
        
        return date1 <= date2
        

