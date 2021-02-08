'''Classes for the reepresentation of a Rubik's Cube'''

import numpy as np

class Piece:
    '''Class for a cube piece'''
    def __init__(self,colour1,colour2,colour3,orientation,position):
        self.colour = (colour1,colour2,colour3)
        #colourz is None if edge piece, colourz and coloury are None if centre piece

        self.orientation = orientation
        #3x3 matrix referring to the 3 vectors the coloured faces point
        #If colour doesn't exist vector is [0,0,0]

        self.position = position
        self.og_pos = position
        #3d vector relative from the centre of the cube
    
    def rotate(self,matrix):
        self.orientation = np.matmul(matrix,self.orientation)
        self.position = np.matmul(matrix,self.position)

    def get_colour(self,vector):
        '''Gets colour of piece pointing in the direction of vector'''
        for column in range(0,3):
            if np.array_equal(vector,self.orientation[:,column]):
                return self.colour[column]
            

class Cube:
    '''Class for the whole cube'''
    def __init__(self):
        self.vector_face = {(0,0,-1):np.s_[:,:,0],(0,0,1):np.s_[:,:,2],(0,-1,0):np.s_[:,0,:],(0,1,0):np.s_[:,2,:],(-1,0,0):np.s_[0,:,:],(1,0,0):np.s_[2,:,:]}
        #Dictionary of slicing operations
        colour_list = {(0,0,0):None,(1,0,0):0,(-1,0,0):1,(0,1,0):2,(0,-1,0):3,(0,0,1):4,(0,0,-1):5}
        #Converts the direction a side is facing to the original colour of that side (also the same colour as the center piece)
        self.cube = np.empty((3,3,3),dtype=object)
        for piece_pos in [(a,b,c) for a in range(-1,2) for b in range(-1,2) for c in range(-1,2)]:
            #piece_pos = (x,y,z) where -1 <= x,y,z <= 1
            piece_orientation = np.zeros((3,3),dtype=np.int8)
            for a in range(0,3):
                piece_orientation[a,a] = piece_pos[a]
            self.cube[tuple(map(lambda a: a+1, piece_pos))] = Piece(colour_list[tuple(piece_orientation[:,0])], #tuple conversion as np array is not hashable
                                                             colour_list[tuple(piece_orientation[:,1])],
                                                             colour_list[tuple(piece_orientation[:,2])],
                                                             piece_orientation,
                                                             piece_pos)

    def turn(self,vector,direction):
        '''vector is the direction the centre piece of the side points in, direction is 1 for clockwise, -1 for anticlockwise'''
        side = self.cube[self.vector_face[vector]]
        #Describes a rotation matrix to be applied to the slice
        matrix = np.array([[abs(vector[0]),direction*vector[2],-direction*vector[1]],
                           [-direction*vector[2],abs(vector[1]),direction*vector[0]],
                           [direction*vector[1],-direction*vector[0],abs(vector[2])]])
        turned_side = np.empty((3,3,3),dtype=object)
        for x in range(0,3):
            for y in range(0,3):
                piece = side[x,y]
                piece.rotate(matrix)
                turned_side[tuple(map(lambda a: a+1, piece.position))] = piece #As piece_position coordinates have range -1 to 1 inclusive, while cube indexing has range 0 to 2 inclusive
        self.cube[self.vector_face[vector]] = turned_side[self.vector_face[tuple(vector)]]
    
    def faces(self):
        faces = []
        for vector in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
            face = np.zeros((3,3),np.int8)
            side = self.cube[self.vector_face[vector]]
            for x in range(0,3):
                for y in range(0,3):
                    face[x,y] = side[x,y].get_colour(np.array(vector))
            if (vector in [(-1,0,0),(0,1,0),(0,0,-1)]): #To account for numpy slicing reindexing, and perspective
                face = np.transpose(face)
            faces.append(face)
        return faces


