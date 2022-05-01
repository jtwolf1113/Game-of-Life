import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML 



plt.rcParams['figure.figsize']=[22,22] #increase the default figure size
plt.rcParams.update({'font.size':18})
plt.rcParams['animation.embed_limit'] = 400 #set the animation data size to 400 MB (defaults to 20)
plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\jaket\Desktop\ffmpeg-2021-06-27-git-49e3a8165c-full_build\bin\ffmpeg.exe'
Writer = animation.writers['ffmpeg']
writer = Writer(fps=10, metadata=dict(artist='Me'), bitrate=1800)

class Life:
    #if no lattice is input create a default one
    def generate_Random_Lattice(self, xlen = None, ylen = None):
        if xlen is None and ylen is None:
            xmax = 20
            ymax = 20
        elif xlen and ylen:
            xmax = xlen
            ymax = ylen

        lattice = {}
        for i in range(-xmax,xmax,1):
            lattice[i] = {}
            for j in range(-ymax,ymax,1):
                lattice[i][j] = np.random.randint(0,2)
        return lattice


    #use init to set system bounds, setup the initial dictionary 
    def __init__(self, inputMat = None, xlen = None, ylen = None): #input Mat is a dictionary where the indices are the coordinates
        
        if inputMat is not None:
            self.lattice = inputMat
        elif inputMat is None:
            if xlen is not None and ylen is not None:
                self.lattice = self.generate_Random_Lattice(xlen=xlen, ylen=ylen)
            elif xlen is not None:
                self.lattice = self.generate_Random_Lattice(xlen = xlen, ylen = xlen)
            elif ylen is not None:
                self.lattice = self.generate_Random_Lattice(xlen=ylen, ylen = ylen)
            else:
                self.lattice = self.generate_Random_Lattice()

        if xlen == None:
            xmin = -int(len(self.lattice)/2)
            xmax = int(len(self.lattice)/2)
            if len(self.lattice)%2 ==1:
                xmax += 1
        else:
            xmin = -int(xlen/2)
            xmax = int(xlen/2)
            if (xlen)%2 ==1:
                xmax += 1
        if ylen == None:
            ymin = -int(len(self.lattice[0])/2)
            ymax = int(len(self.lattice[0])/2)
            if len(self.lattice[0])%2 ==1:
                ymax += 1
        else: 
            ymin = -int(ylen/2)
            ymax = int(ylen/2)
            if len(ylen)%2 ==1:
                ymax += 1
                
        self.xlen = len(self.lattice)
        self.ylen = len(self.lattice[0])
        self.xmin = int(xmin)
        self.xmax = int(xmax)
        self.ymin = int(ymin)
        self.ymax = int(ymax)
        
        self.ax = plt.subplots()
    
   
    
    #animate the 
    def animateIt(self, intervals, fcount, inline = False, filename = 'Life', style = None):
        if style is None:
            style = 'ks'
         #function to update each frame in the animation
        def frame(q):
            #reset the data to be plotted 
            xdata = []
            ydata = []
            count = {}
           
            #reset the neighbor count dicitionary values
            for i in range(self.xmin,self.xmax,1):
                count[i] = {}
                for j in range(self.ymin,self.ymax,1):
                    count[i][j] = 0

            #Count all of the neighbors for each cell
            for i in range(self.xmin,self.xmax,1):
                for j in range(self.ymin,self.ymax,1):
                    if j < self.ymax-1:
                        if self.lattice[i][j+1] == 1:
                            count[i][j] += 1
                    if j > self.ymin:
                        if self.lattice[i][j-1] == 1:
                            count[i][j] += 1
                    if i < self.xmax-1:
                        if self.lattice[i+1][j] == 1:
                            count[i][j] += 1
                    if i > self.xmin:
                        if self.lattice[i-1][j] == 1:
                            count[i][j] += 1
                    if i < self.xmax-1 and j < self.ymax-1:
                        if self.lattice[i+1][j+1] == 1:
                            count[i][j] += 1
                    if i > self.xmin and j < self.ymax-1:
                        if self.lattice[i-1][j+1] == 1:
                            count[i][j] += 1
                    if i > self.xmin and j > self.ymin:
                        if self.lattice[i-1][j-1] == 1:
                            count[i][j] += 1
                    if i < self.xmax-1 and j > self.ymin:
                        if self.lattice[i+1][j-1] == 1:
                            count[i][j] += 1

            #apply rules of life
            for i in range(self.xmin,self.xmax,1):
                for j in range(self.ymin,self.ymax,1):
                    if self.lattice[i][j] == 1:
                        if count[i][j]>3:
                            self.lattice[i][j] = 0
                        elif count[i][j] < 2:
                            self.lattice[i][j] = 0
                    if self.lattice[i][j] == 0:
                        if count[i][j] == 3:
                            self.lattice[i][j] = 1

            #Plot lattice values with 1 as they are alive
            for i in range(self.xmin,self.xmax,1):
                for j in range(self.ymin,self.ymax,1):
                    if self.lattice[i][j] == 1:
                        xdata.append(i)
                        ydata.append(j)
            line, = self.line
            line.set_xdata(xdata)
            line.set_ydata(ydata)
            self.line = line,
            return line,
        #now we generate the plot and animate it         
        fig, ax = self.ax
        xdata = []
        ydata = []
        self.line = ax.plot([],[], style)
        ax.set_xlim(-self.xmax,self.xmax)
        ax.set_ylim(-self.ymax,self.ymax)
        ax.set_title('Game of Life')
        ax.set_xlabel('X coordinate')
        ax.set_ylabel('Y coordinate')
        count = {}
        
        anim = animation.FuncAnimation(fig, frame, frames = fcount, interval = intervals,blit = True)
        plt.close()
        if inline:
            return HTML(anim.to_jshtml())
        else:
            anim.save(filename+'.mp4', writer = writer)




if __name__ == '__main__':
    #generate a lattice of size 100x100
    Random_Game = Life(xlen=100) 
    #animate the lattice for 600 frames with 200 ms intervals, then save it (inline=false) as 'Life_2.mp4', color the organisms magenta with a square shape 
    Random_Game.animateIt(intervals = 200, fcount = 600, inline = False, style = 'ms',filename='Life_2')    
