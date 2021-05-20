import snap

class graphRandom:
    graphs=[]
    
    def __init__(self):
        self.allGraphs()
        self.properties()

    
    def properties(self):
        for i in self.graphs:
            for EI in i.Edges():
                print("edge: (%d, %d)" % (EI.GetSrcNId(), EI.GetDstNId()))

    
    def allGraphs(self):
        #loading of ten graphs to mine - Im sure there is faster way to go across the data set #.edges gives ego network - how many friendships person has
        self.G1 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
        self.G2 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
        self.G3 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
        self.G4 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
        self.G5 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
        self.G6 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
        self.G7 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
        self.G8 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
        self.G9 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
        self.G10 = snap.GenRndGnm(snap.TUNGraph, 10000, 5000,False)
    
        self.graphs=[self.G1,self.G2,self.G3,self.G4,self.G5,self.G6,self.G7,self.G8,self.G9,self.G10] ##
    
        
    

graphRandom()
        
