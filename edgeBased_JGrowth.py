import snap

class edgeBased_JGrowth:
    main_graph=snap.TUNGraph.New()
    

    def __init__(self):
        #dictionary for single graphs
        freq_singleton_graph={}   
        edge_count=int(88234) 
    
        #loading and populating of undirected graph
        print('creating graph and loading text file')
        G5=snap.TUNGraph.New()
        G5 = snap.LoadEdgeList(snap.TUNGraph, "datasets/facebook_combined.txt", 0, 1)
        print("G5: Nodes %d, Edges %d" % (G5.GetNodes(), G5.GetEdges()))

        #adding the circles of friends 

        
        #singleton list
        for EI in G5.Edges():
            edge = (EI.GetSrcNId()), (EI.GetDstNId())
            print(edge)
            if edge in freq_singleton_graph:
                print('hi')
                freq_singleton_graph[edge]+=1
            else:freq_singleton_graph[edge]=1
        
        for key in freq_singleton_graph.keys():
            print("Key : {} , Value : {}".format(key,freq_singleton_graph[key]))
        
        print("calculating frequencies")
        sort_freq_graph=[]
        
        for (candidate1,candidate2), value in sorted(freq_singleton_graph.items(), key=lambda x: x[1], reverse=True):
            print(candidate1, candidate2)
            frequency = (int(freq_singleton_graph[candidate1, candidate2])) / (edge_count)
            if frequency >= .000001:
               sort_freq_graph.append((candidate1,candidate2, frequency))
       
       #sorted list of singleton graphs in F1 (contain one single edge each)
        for (item1,item2, freq) in sort_freq_graph:
          print(f"{item1,item2},{freq}")

    
    


    ##def count():
      ##  print("hi") #traverse the edges  - could later use for mutual friends count
        

X=edgeBased_JGrowth()
