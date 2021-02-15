import numpy as np
import dataset

class Layer:
    def __init__(self,input_size,output_size,alpha,is_first_layer = True,input = None):
        self.alpha = alpha #this is the training rate of the network
        self.first_layer = is_first_layer #If first layer, in gradient_descent doesn't call previous layer
        self.input = input                #Stores layer preceding this layer
        self.z = np.zeros((output_size,1)) #stores value nodes before non-linear sigmoid
        self.node_values = np.zeros((output_size,1))            
        self.weights = np.random.normal(0,(1/(input_size**0.5)),(output_size,input_size)) #Xavier initialisation of values
        self.biases = np.zeros((output_size,1))
        self.input_values = np.zeros((input_size,1)) #stores inputs needed for gradient descent
        self.dweights = []  #Stores changes in weights and biases for mini-batch gradient descent
        self.dbiases = []

    def sigmoid(self,x):
        return 1/(1 + np.exp(-x))
    
    def sigmoid_derivative(self,x):
        return 1/(2 + np.exp(-x) + np.exp(x))

    def evaluate(self,input_values):
        self.z = np.matmul(self.weights,input_values) + self.biases
        self.node_values = self.sigmoid(self.z)
        self.input_values = input_values
        return self.node_values
    
    def cost_derivative(self,dcostoutput):
        dsigmoid = self.sigmoid_derivative(self.z)                                      #dsigmoid(z)/dz     (note dsigmoid(z) = output)
        dweights = np.matmul(dsigmoid*dcostoutput,np.transpose(self.input_values)) #(dcost/output)*(dsigmoid(z)/dz)*(dz/dweight)
        dbiases = dsigmoid*dcostoutput
        if not self.first_layer:
            dinputs = np.matmul(np.transpose(self.weights),dsigmoid*dcostoutput) #summed over different z (dcost/output)*(dsigmoid(z)/dz)*(dz/dinputs)
            self.input.cost_derivative(dinputs)
        self.dweights.append(dweights)
        self.dbiases.append(dbiases)
    
    def gradient_descent(self):
        self.weights -= self.alpha*np.average(self.dweights,axis = 0)
        self.biases -= self.alpha*np.average(self.dbiases,axis = 0)
        #print(self.alpha*np.average(self.dweights,axis = 0))
        self.dweights = []
        self.dbiases = []


class NeuralNetwork:
    def __init__(self,layer_shapes,dataset = None,alpha = 1): #layer_shapes an array of the shape of the weights matrix
        if len(layer_shapes) == 0:
            raise Exception("Need the shape of at least an input and an output layer")
        self.alpha = alpha
        self.dataset = dataset
        self.layers = [Layer(layer_shapes[0],layer_shapes[1],self.alpha)]
        self.input_size = layer_shapes[0]
        self.output_size = layer_shapes[-1]
        for i in range(1,len(layer_shapes)-1):
            self.layers.append(Layer(layer_shapes[i],layer_shapes[i+1],self.alpha,is_first_layer=False,input=self.layers[-1]))
    
    def evaluate(self,input_vector):
        next_input = np.array(input_vector).reshape(self.input_size,1) #variable passes values 
        for layer in self.layers:
            next_input = layer.evaluate(next_input)
        return next_input #at this point it is the output of the last layer
        
    def set_dataset(self,dataset):
        self.dataset = dataset

    def SGD_dataset(self,batch_size):
        training_data = self.dataset.get_training_data_batch(batch_size)
        costs = []          #eventually could be used for a graph plot
        for input_vector,expected_output in training_data:
            network_value = self.evaluate(input_vector)
            cost = np.sum((network_value - np.array(expected_output).reshape(self.output_size,1))**2)
            costs.append(cost)
            dcostinput = 2*(network_value - np.array(expected_output).reshape(self.output_size,1))   #change in cost relative to change in input      
            self.layers[-1].cost_derivative(dcostinput)    #This will call cost_derivative in previous layers through back propogation
        print(costs)
        for layer in self.layers:
            layer.gradient_descent()                   #Applies changes to network parameters

    def SGD_on_input(self,input_vector,expected_output):
        network_value = self.evaluate(input_vector)
        cost = np.sum((network_value - np.array(expected_output).reshape(self.output_size,1))**2)
        print(cost)
        dcostinput = 2*(network_value - np.array(expected_output).reshape(self.output_size,1))   #change in cost relative to change in input      
        self.layers[-1].cost_derivative(dcostinput)    #This will call cost_derivative in previous layers through back propogation
        for layer in self.layers:
            layer.gradient_descent()                   #Applies changes to network parameters