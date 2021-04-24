import snap

class nodeBased_JGrowth:
    main_graph = snap.TUNGraph.New()
    

    def __init__(self):
        #dictionary for single graphs
        freq_singleton_graph={}
        
        fpg = {}
        
        #loading and populating of undirected graph
        print('creating graph and loading text file')
        G2 = snap.TUNGraph.New()
        G2 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook_combined.txt", 0, 1)
        
        # traverse the nodes (singleton list)
        for NI in G2.Nodes():
            print("node id %d" % (
                NI.GetId()))
            
        # count nodes
        print(G2.Nodes())
        
        # print nodes and edges
        #print("G2: Nodes %d, Edges %d" % (G2.GetNodes(), G2.GetEdges()))
        
        #singleton list
        for NI in G2.Edges():
            pair = (NI.GetSrcNId()), (NI.GetDstNId())
            #print(pair)
            
       
            if pair in freq_singleton_graph:
                print('hi')
                freq_singleton_graph[pair]+=1
            else:freq_singleton_graph[pair]=1
        
        
        
        

X=nodeBased_JGrowth()