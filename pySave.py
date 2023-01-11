import os 
import json 

class Save_Manager:
    def __init__(self, folder, file_name):
        self.path = folder  + "/"
        self.fn = file_name

        try:

            try:
                os.mkdir(self.path)
            except:
                print("folder already created")
            try:
                with open(self.path + self.fn + ".json", "r") as file:
                    self.saved = json.load(file)
            except:   
                self.saved = {}
            print("created file")
        except FileExistsError:
            print("Folder/File already exists")
            with open(self.path+self.fn+".json", "r") as file:
                self.saved = json.load(file)
    
    def save(self, varname, var):
        self.saved[varname] = var

    def load(self,varname):
        with open(self.path + self.fn + ".json", "r") as file:
            temp_dict = json.load(file)
            try:
                return temp_dict[varname]
            except KeyError:
                return Exception(f"Invalid Variable Name : {varname} or var was never saved")

    def apply(self):
        with open(self.path + self.fn + ".json", "w") as file:
            json.dump(self.saved, file)

if __name__ == '__main__':
    sm = Save_Manager("save_data/", "data")
    sm2 = Save_Manager("save_data/", "data2")


    sm.save("nigga", "1")
    sm2.save("nigga", "2")

    sm.apply()
    sm2.apply()