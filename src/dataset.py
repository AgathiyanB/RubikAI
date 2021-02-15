import numpy as np
import json

class DataSet:
    def __init__(self):
        self.training_data = []
        self.validation_data = []
        self.test_data = []
        self.traind_index = 0
        self.validd_index = 0
        self.testd_index = 0

    def save_data(self,fname):
        data = {"training" : self.training_data,
                "validation" : self.validation_data,
                "test" : self.test_data}
        file = open(fname,"w")
        json.dump(data,file)
        file.close()

    def load_data(self,fname):
        file = open(fname,"r")
        data = json.load(file)
        file.close()
        self.training_data = data["training"]
        self.validation_data = data["validation"]
        self.test_data = data["test"]

    def get_training_data_batch(self,batch_size):
        if batch_size > len(self.training_data):
            raise Exception("Batch size too big")
        if self.traind_index+batch_size >= len(self.training_data):
            self.traind_index = 0
        data = self.training_data[self.traind_index:self.traind_index+batch_size]
        self.traind_index += batch_size
        return data

    def get_validation_data(self):
        return self.validation_data

    def get_test_data(self):
        return self.test_data

    def remove_training_data(self,index):
        del self.training_data[index]
    
    def remove_validation_data(self,index):
        del self.training_data[index]
    
    def remove_test_data(self,index):
        del self.training_data[index]

    def append_training_data(self,input_vector,output_vector):
        self.training_data.append((input_vector,output_vector))

    def append_validation_data(self,input_vector,output_vector):
        self.validation_data.append((input_vector,output_vector))

    def append_test_data(self,input_vector,output_vector):
        self.test_data.append((input_vector,output_vector))
