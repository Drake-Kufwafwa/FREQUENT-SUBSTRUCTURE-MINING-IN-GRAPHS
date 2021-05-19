import snap

class graph_Exploration:
    graphs=[]
    
    def __init__(self):
        self.allGraphs()

        G=snap.TUNGraph.New()
        G = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook_combined.txt", 0, 1)
        print("G: Nodes %d, Edges %d" % (G.GetNodes(), G.GetEdges()))

        self.properties()
    
    def allGraphs(self):
        #loading of ten graphs to mine - Im sure there is faster way to go across the data set #.edges gives ego network - how many friendships person has
        self.G1 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/0.edges", 0, 1)
        self.G2 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/107.edges", 0, 1)
        self.G3 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/348.edges", 0, 1)
        self.G4 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/414.edges", 0, 1)
        self.G5 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/686.edges", 0, 1)
        self.G6 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/698.edges", 0, 1)
        self.G7 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/3437.edges", 0, 1)
        self.G8 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/1912.edges", 0, 1)
        self.G9 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/3437.edges", 0, 1)
        self.G10 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook/3980.edges", 0, 1)
    
        self.graphs=[self.G1,self.G2,self.G3,self.G4,self.G5,self.G6,self.G7,self.G8,self.G9,self.G10] ##
    
    def properties(self):
        
    

graph_Exploration()
        
