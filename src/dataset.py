import numpy as np
import json

class DataSet:
    def __init__(self):
        self.training_data = np.empty(0)
        self.validation_data = np.empty(0)
        self.test_data = np.empty(0)
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
        self.training_data = np.array(data["training"])
        self.validation_data = np.array(data["validation"])
        self.test_data = np.array(data["test"])

    def get_training_data_batch(self,batch_size):
        data = self.training_data[self.traind_index:self.traind_index+batch_size]
        self.traind_index += batch_size
        return data

    def get_validation_data(self):
        return self.validation_data

    def get_test_data(self):
        return self.test_data

    def append_training_data(self,input_vector,output_vector):
        np.append(self.training_data,[[input_vector,output_vector]],axis = 0)

    def append_validation_data(self,input_vector,output_vector):
        np.append(self.validation_data,[[input_vector,output_vector]],axis = 0)

    def append_test_data(self,input_vector,output_vector):
        np.append(self.test_data,[[input_vector,output_vector]],axis = 0)