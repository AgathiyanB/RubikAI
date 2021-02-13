import numpy as np

class Layer:
    def __init__(self,input_size,output_size,is_first_layer = True,input = None):
        self.first_layer = is_first_layer #If first layer, in gradient_descent doesn't call previous layer
        self.input = input                #Stores layer preceding this layer
        self.z = np.zeros((output_size,1)) #stores value nodes before non-linear sigmoid
        self.node_values = np.zeros((output_size,1))            
        self.weights = np.random.normal(0,(1/input_size),(output_size,input_size)) #Xavier initialisation of values
        self.biases = np.zeros((output_size,1))
        self.input_values = np.zeros((input_size,1)) #stores inputs needed for gradient descent

    def sigmoid(self,x):
        return 1/(1 + np.exp(-x))
    
    def sigmoid_derivative(self,x):
        return 1/(2 + np.exp(-x) + np.exp(x))

    def evaluate(self,input_values):
        self.z = np.matmul(self.weights,input_values) + self.biases
        self.node_values = self.sigmoid(self.z)
        self.input_values = input_values
        return self.node_values
    
    def gradient_descent(self,dcostoutput):
        dsigmoid = self.sigmoid_derivative(self.z)                                      #dsigmoid(z)/dz     (note dsigmoid(z) = output)
        dweights = np.matmul(dsigmoid*dcostoutput,np.transpose(self.input_values)) #(dcost/output)*(dsigmoid(z)/dz)*(dz/dweight)
        print(dweights)
        dbiases = dsigmoid*dcostoutput                                                  #(dcost/output)*(dsigmoid(z)/dz)*(dz/dwbiases)
        print(dbiases)
        if not self.first_layer:
            dinputs = np.matmul(self.weights,dsigmoid*dcostoutput) #summed over different z (dcost/output)*(dsigmoid(z)/dz)*(dz/dinputs)
            self.input.gradient_descent(dinputs)
        self.weights -= dweights
        self.biases -= dbiases


class NeuralNetwork:
    def __init__(self,layer_shapes): #layer_shapes an array of the shape of the weights matrix
        if len(layer_shapes) == 0:
            raise Exception("Need the shape of at least an input and an output layer")
        self.layers = [Layer(layer_shapes[0],layer_shapes[1])]
        self.input_size = layer_shapes[0]
        self.output_size = layer_shapes[-1]
        for i in range(1,len(layer_shapes)-1):
            self.layers.append(Layer(layer_shapes[i],layer_shapes[i+1],is_first_layer=False,input=self.layers[-1]))
    
    def evaluate(self,input_vector):
        next_input = np.array(input_vector).reshape(self.input_size,1) #variable passes values 
        for layer in self.layers:
            next_input = layer.evaluate(next_input)
        return next_input #at this point it is the output of the last layer
        

    def train_network(self,input_vector,desired_values):
        network_value = self.evaluate(input_vector)
        dcostinput = 2*(network_value - np.array(desired_values).reshape(self.output_size,1))   #change in cost relative to change in input      
        self.layers[-1].gradient_descent(dcostinput)    #This will call gradient_descent in previous layers through back propogation