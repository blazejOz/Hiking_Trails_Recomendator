import csv

class RouteDataManager:
    
    @staticmethod
    def load_trails(filePath):
        '''
            ladowanie tras z pliku csv(gotowego)
        '''

        trails = []
        with open(filePath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                trails.append(row)
        print("trails loaded")
        return trails