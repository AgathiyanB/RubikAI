#Use tkinter frame and a net
import cube
import tkinter as tk
#Input cube, Output frame containing a net

'''faces is a 3d array, or more clearly a 1d array or 2d faces'''
def create_net(master,faces):
    '''creates the net of cube'''
    frame = tk.Frame(master)
    position = {0:(1,1),1:(3,1),2:(1,2),3:(1,0),4:(0,1),5:(2,1)}
    rotation = {0:3,1:0,2:2,3:3,4:0,5:3}
    #Number of clockwise rotations to set the face in the right orientation
    #A 4d array referring to all of the stickers on the cube
    labels = []
    for i in range(0,6):
        (a,b) = position[i]
        subframe, subframelabels = create_subframe(frame,faces[i],rotation[i])
        subframe.grid(row=a,column=b)
        labels.append(subframelabels)
    return (frame,labels)

def create_subframe(master,face,rotation):
    '''creates the three by three grids'''
    frame = tk.Frame(master)
    colour = {0:"white",1:"yellow",2:"red",3:"orange",4:"blue",5:"green"}
    labels = []
    for i in range(0,3):
        row = []
        for j in range(0,3):
            label = tk.Label(frame, width = 2, height = 1, relief = tk.RAISED, bg = colour[face[i,j]])
            if rotation == 0:
                label.grid(row = i, column = j)
            elif rotation == 2:
                label.grid(row = 2-i, column = 2-j)
            else: #rotation == 3
                label.grid(row = 2-j, column = i)
            row.append(label)
        labels.append(row)
    return (frame,labels)

def update_labels(c,labels):
    colour = {0:"white",1:"yellow",2:"red",3:"orange",4:"blue",5:"green"}
    faces = c.faces()
    for i in range(0,6):
        for j in range(0,3):
            for k in range(0,3):
                labels[i][j][k].config(bg = colour[faces[i][j][k]])


def button_turn(c,vector,direction,labels):
    c.turn(vector,direction)
    update_labels(c,labels)


if __name__ == "__main__":
    root = tk.Tk()
    c = cube.Cube()
    frame, labels = create_net(root,c.faces())
    frame.grid(row = 0, columnspan = 6)
    #
    tk.Button(root, text = "F", command = (lambda : button_turn(c,(1,0,0),1,labels))).grid(row = 1, column = 0)
    tk.Button(root, text = "F'", command = (lambda : button_turn(c,(1,0,0),-1,labels))).grid(row = 2, column = 0)
    tk.Button(root, text = "B", command = (lambda : button_turn(c,(-1,0,0),1,labels))).grid(row = 1, column = 1)
    tk.Button(root, text = "B'", command = (lambda : button_turn(c,(-1,0,0),-1,labels))).grid(row = 2, column = 1)
    tk.Button(root, text = "R", command = (lambda : button_turn(c,(0,1,0),1,labels))).grid(row = 1, column = 2)
    tk.Button(root, text = "R'", command = (lambda : button_turn(c,(0,1,0),-1,labels))).grid(row = 2, column = 2)
    tk.Button(root, text = "L", command = (lambda : button_turn(c,(0,-1,0),1,labels))).grid(row = 1, column = 3)
    tk.Button(root, text = "L'", command = (lambda : button_turn(c,(0,-1,0),-1,labels))).grid(row = 2, column = 3)
    tk.Button(root, text = "U", command = (lambda : button_turn(c,(0,0,1),1,labels))).grid(row = 1, column = 4)
    tk.Button(root, text = "U'", command = (lambda : button_turn(c,(0,0,1),-1,labels))).grid(row = 2, column = 4)
    tk.Button(root, text = "D", command = (lambda : button_turn(c,(0,0,-1),1,labels))).grid(row = 1, column = 5)
    tk.Button(root, text = "D'", command = (lambda : button_turn(c,(0,0,-1),-1,labels))).grid(row = 2, column = 5)
    root.mainloop()
    
