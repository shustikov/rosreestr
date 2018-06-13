import os
from report import Report

# to mapping module
class Header:

    def __init__(self, city, street, building):
        self.street = street
        self.building = building
        self.city = city


class DataInstance:

    def __init__(self, resp, owner_obj):
        self.number = resp.apartment
        self.c_num = resp.c_num
        self.area = str(resp.area).replace(".", ",")
        self.fio = owner_obj.fio
        self.regnum = owner_obj.regnumber 
        self.vouts = str(owner_obj.vouts).replace(".", ",")
        self.date = owner_obj.regdate
        self.share = owner_obj.share
        self.floor = resp.floor


class RosReestrReport(Report):

    def __init__(self, template_path, res_folder, city, street):
        street = street.replace("/", "-")
        self.path = os.path.join(res_folder, city, street, street+".xlsx")
        self.street = street
        self.city = city
        Report.__init__(self, self.path, template_path)

    @classmethod
    def set_number_format(cls, cell):
        if cell.coordinate[0] == "F":
            cell.number_format = "0,000"
   

    def add_worksheet(self, resp_list, building):
        header = Header(self.city, self.street, building)
        data = []

        for resp in resp_list:
            for owner in resp.owner_objs:
                di = DataInstance(resp, owner)
                data.append(di)

        Report.add_worksheet(self, header, data, building)		

if __name__ == '__main__':

    from paths import *
    import glob
    from xml_unpuck import Responce

    list_xmls = glob.glob(tmp_folder + '/*.xml')
    resp_list = [Responce(path) for path in list_xmls]
    resp_list = sorted(resp_list, key = lambda x: int(x.apartment))


    d = {}
    for resp in resp_list:

        if resp.street not in d.keys():
            d.update({resp.street : {resp.building : [resp]}})

        elif resp.building not in d[resp.street].keys():
            d[resp.street].update({resp.building : [resp]})

        else:
            d[resp.street][resp.building].append(resp)
        


    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.xlsx") 
    for street, street_resps in d.items():
        report_file =  RosReestrReport(template_path, res_folder, street)  
        for building, building_resps in street_resps.items():
            report_file.add_worksheet(building_resps, building)

        report_file.close()	