from datetime import datetime

from ai_models.deid.date_patterns import date_patterns
import  re
class DateUtils:
    def __init__(self):
        self.date_patterns = date_patterns

    def parse_date(self, date_string):
        
        for  key, pattern in self.date_patterns.items():
            matcher = re.compile(pattern)
            mo = matcher.search(date_string.lower())
            if mo is not None:
                try:
                    # print(datetime.strptime(date_string, key))
                     
                    return True , datetime.strptime(date_string, key)
                except ValueError:
                    print('Not a valid date')
                    return False , ""
            
        return False , ""
                


    def is_valid_date(self, date_string):
        try:
            d = { "st": "", "nd": "", "th":"","rd":""}
            date_suffix = {"nd": "", "th":"","rd":""}
            if "August" not in date_string:
                for x,y in d.items():
                    date_string = date_string.replace(x, y)
            else:
                for x,y in date_suffix.items():
                    date_string = date_string.replace(x, y)
            return self.parse_date(date_string)
        except Exception:
            print('parsing issue')
if __name__ == '__main__':
    date = DateUtils()
    print(date.is_valid_date('aclesun'))


