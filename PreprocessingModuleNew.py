import csv
import numpy as np
import config as params
class Data():
    def __init__(self, filename:str):
        self.multiple = self.get_multiple_data(filename)
        self.single = self.get_single_data(filename)
        self.multiple_splitted = self.data_split(self.multiple, params.Fd)
        self.single_splitted = self.data_split(self.single, params.Fh)
        self.multiple_splitted, self.single_splitted = self.clean(self.multiple_splitted, self.single_splitted)
        self.final_first = self.multiple_to_np(self.multiple_splitted)
        self.final_second = self.single_to_np(self.single_splitted)
        pass
    # Получение всех параметров и даты в отдельный массив
    def get_multiple_data(self, filename:str):
        data = []
        with open(filename, encoding='cp1251') as file:
            file_reader = csv.reader(file, delimiter = ';')
            for i, row in enumerate(file_reader):
                if i == 0:
                    continue
                if row[6] != '' and row[7]!='' and row[8]!='' and row[1]=='3000014':
                    data.append([row[3], int(row[4]), int(row[6]), int(row[7]), int(row[8])])
                if row[3] == '25.04.2020':
                    break
        return data[3:]
    # Получение даты и уровня воды в отдельный массив
    def get_single_data(self, filename:str):	
        data = []
        with open(filename, encoding='cp1251') as file:
            file_reader = csv.reader(file, delimiter = ';')
            for i, row in enumerate(file_reader):
                if i == 0:
                    continue
                if row[6] != '' and row[7]!='' and row[8]!='' and row[1]=='3000014':
                    data.append([row[3], int(row[4])])
                if row[3] == '25.04.2020':
                    break
        return data[3:]
    # Разбивка на пятидневки
    def data_split(self, data:list, n:int):
        counter = 0
        newdata = []
        temp_array = []
        for array in data:
            counter += 1
            temp_array.append(array)
            if counter % n == 0:
                newdata.append(temp_array)
                temp_array = []
        return newdata
    # Выборка через один элемент для каждого массива
    def clean(self, multiple_data:list, single_data:list):
        return multiple_data[:-1], single_data[1:]
    # Функции превращения списков в массивы numpy
    def multiple_to_np(self, data:list):
        arr = np.zeros((len(data),params.Fd,4))
        for i in range(len(data)):
            for j in range(params.Fd):
                for k in range(4):
                    arr[i][j][k] = data[i][j][k+1]
        return arr
    def single_to_np(self, data:list):
        arr = np.zeros((len(data),params.Fh))
        for i in range(len(data)):
            for j in range(params.Fh):
                arr[i][j] = data[i][j][1]
        return arr
obj = Data('Urovni2_1_1_new.csv')
''' multiple - это данные с 5 параметрами, дата, уровень воды, температура, скорость воздуха;
    single - это данные с 2 параметрами, дата, уровень воды;
    splitted - данные, разбитые на пятидневки;
    final - финальная версия данных, массив numpy без дат
'''
# Предварительные данные
multiple = obj.multiple_splitted
single = obj.single_splitted
print(len(multiple), len(single))
for c in multiple:
    print(c)
for c in single:
    print(c)
# Данные без дат
print('-'*50)
first = obj.final_first
second = obj.final_second
