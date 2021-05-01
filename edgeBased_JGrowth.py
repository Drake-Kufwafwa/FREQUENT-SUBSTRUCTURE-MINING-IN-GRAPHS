import snap


class edgeBased_JGrowth:
    CK=[]
    graphs=[] #updated on call to allgraphs
    singleton_edges={}
    edge_support={}
    edges={} 
    
    def __init__(self):    
        #loading and populating of undirected graph creating self.graphs
        print('creating graph and loading text file')

        #create ten graphs == ten users
        self.allGraphs()
                  
        #large graph with all edges
        G=snap.TUNGraph.New()
        G = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook_combined.txt", 0, 1)
        print("G: Nodes %d, Edges %d" % (G.GetNodes(), G.GetEdges()))

        singleton_edges=self.singleton(G) #creates dictionary of all edges and edge supports
        count=0
       
        #look for minimum of 3 similar friends/edges
        ego_subgraphs={}

        '''
        #iterate each ego network and update counts into the graph matrix
        graph_id_count=0 #start at first list of edges from graph id 1
        for edge in self.edge[graph_id_count]: #for each ego network's edges(graphids) in edges dictionary update the the graph matrix at {starting at id 1}
                edge in self.edge[graph_id_count] #hash each edge into the matrix at a value

                #create new itemset
                 = set(edge_set)

                #union itemsets
        '''
                

                #if hash exists add to the ego_subgraph at hash of edge
        ##graph_id_count++



        k=1
        L=[singleton_edges]
        sorted_CK=self.compute_cSubgraph(L, k=k)
        for i in sorted_CK:
            print(i)
        

    
    
    def singleton(self, Graph):
        freq_singleton_graph={}   
        edge_count=int(88234) 

        ##join edges in graph 
        for EI in Graph.Edges():
            edge = (EI.GetSrcNId()), (EI.GetDstNId())
            print(edge)
            if edge in freq_singleton_graph:
                print('hi')
                freq_singleton_graph[edge]+=1
            else:freq_singleton_graph[edge]=1
        
        #dubug
        for key in freq_singleton_graph.keys():
            print("Key : {} , Value : {}".format(key,freq_singleton_graph[key]))
        
        id_count=0
        #calculate supports of edges in all ego networks
        for key in freq_singleton_graph.keys(): ##list of all edges starting at first edge
            print(key)
            ##look at all occurances in ego networks starting at id 0
            for ego_network in self.graphs:
                id_count+=1
                #edge count - print (ego_network.GetEdges())
                # #edge list of edges from each  ego network
                
                for EI in ego_network.Edges():
                    curr_edge=(EI.GetSrcNId(), EI.GetDstNId())
                    if (str(curr_edge)==(key)):
                        self.edge_support[key]+=1
                    else:self.edge_support[key]=1

        
        print("calculating frequencies")
        sort_freq_graph=[]
        
        for (candidate1,candidate2), value in sorted(self.edge_support.items(), key=lambda x: x[1], reverse=True):
            print(candidate1, candidate2)
            frequency = (int(self.edge_support[candidate1, candidate2])) / (edge_count)
            if frequency >= .000001:
               sort_freq_graph.append((candidate1,candidate2, frequency))
       
       #sorted list of singleton graphs in F1 (contain one single edge each)
        for (item1,item2, freq) in sort_freq_graph:
            print(f"{item1,item2},{freq}")
        
        
        #returns the list 
        self.sort_freq_graph=sort_freq_graph
        return sort_freq_graph
        
    
    def compute_cSubgraph(self, g1_candidates, k):
        print("candidiate generation")
        
        #create graph for item and look in dataset to find candidate edges 
        k=1
        LK_= self.sort_freq_graph
        CK = []
        print(LK_)

        ##traverse all possible edge subsets
        for i in range(len(LK_)):
            for j in range(i+1, len(LK_)): # enumerate all combinations in the Lk-1 itemsets
                L1 = sorted(list(LK_[i]))[:k-2]
                L2 = sorted(list(LK_[j]))[:k-2]
                if L1 == L2: # if the first k-1 terms have the same edges the same in two subgraphs, merge the two itemsets
                    new_candidate = list(set(LK_[i]) | set(LK_[j])) # set union
                    CK.append(new_candidate) 
                    print("printing k-1 candidates")
                    print(CK)
                    return sorted(CK)
    
    def allGraphs(self):
        #loading of ten graphs to mine - Im sure there is faster way to go across the data set 
            #.edges gives ego network - how many friendships person has
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
        

        



            

        
edgeBased_JGrowth()

