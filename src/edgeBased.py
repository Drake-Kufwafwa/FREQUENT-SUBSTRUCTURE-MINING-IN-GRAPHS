import snap
# Edge-based Join Growth

class edgeBased:
    def __init__(self) -> None:
        self.g=get_graph_database
        self.minsup = 4
        self.edge_based_join_growth(self.g, self.minsup)
        

    def get_frequent_singleton_graphs_EB(ES, minsup):
        F1 = {}
        for E in ES:
            if ES[E] >= minsup:
                subgraph = snap.TUNGraph.New()
                subgraph.AddNode(E[0])
                subgraph.AddNode(E[1])
                subgraph.AddEdge(E[0], E[1])
                F1[subgraph] = ES[E]
        return F1
    
    def subgraph_match_EB(sG1, sG2): 
        nmE_f = False # non-matching node found
        nmE = None # non-matching edge
    
        for E in sG1.Edges():
            if not sG2.IsEdge(E.GetSrcNId(), E.GetDstNId()):
                if nmE_f:
                    nmE_f = False
                    break
                else:
                    nmE = (E.GetSrcNId(), E.GetDstNId())
                    nmE_f = True
    
        if nmE_f:
            if sG2.IsNode(nmE[0]) and sG2.IsNode(nmE[1]):
                print("A")
                return True, nmE, None
            elif sG2.IsNode(nmE[0]):
                print("B")
                return True, nmE, nmE[1]
            elif sG2.IsNode(nmE[1]):
                print("C")
                return True, nmE, nmE[0]
    
        return False, None, None
    
    
    def join_subgraphs_EB(subgraph1, subgraph2, nmE, nmN):
        c = snap.ConvertGraph(type(subgraph2), subgraph2)
    
        if nmN:
            c.AddNode(nmN)

        c.AddEdge(nmE[0], nmE[1])   

        return c
    
    def generate_candidates_EB(self,Fk, k):
        candidates = []
    
        for i in range(0, len(Fk)):
            sG1 = Fk[i]
        
            for j in range(i+1, len(Fk)):
                sG2 = Fk[j]
#             print("sG1: {}, sG2: {}".format(graph_to_list(sG1), graph_to_list(sG2)))
                match, nmE, nmN = self.subgraph_match_EB(sG1, sG2)
#               print("Match: {}".format(match))
                if match:
                    c = self.join_subgraphs_EB(sG1, sG2, nmE, nmN)
#                 print("C: {}".format(graph_to_list(c)))
                    candidates.append(c)
        print("Candididates {}".format(k))
        for c in candidates:
            print(graph_to_list(c))
        return candidates
                
    def generate_Fkplus1_EB(C, g, minsup): 
        Fkplus1 = {}
        candidate_is_subgraph = True
        support = 0
    
        for candidate in C:
            for graph in g:

                # check if graph contains all candidate's nodes
                for N in candidate.Nodes():
                    if not graph.IsNode(N.GetId()):
                        candidate_is_subgraph = False
                        break

                # check if graph contains all candidate's edges    
                if candidate_is_subgraph:        
                    for E in candidate.Edges():
                        if not graph.IsEdge(E.GetSrcNId(), E.GetDstNId()):
                            candidate_is_subgraph = False
                            break

                # increment support            
                if candidate_is_subgraph:
                    support += 1

                # reset for next graph
                candidate_is_subgraph = True

            if support >= minsup:
                Fkplus1[candidate] = support

            support = 0 # reset support for next candidate
    
        return Fkplus1

    def update_FsG_EB(Fk, FsG):
        exists = True
    
        for G in Fk.keys():  
            for g in FsG.keys():
            
                exists = True
            
                # False if any node or any edge does not match
                for N in G.Nodes():
                    if not g.IsNode(N.GetId()):
                        exists = False
                        break
                for E in G.Edges():
                    if not g.IsEdge(E.GetSrcNId(), E.GetDstNId()):
                        exists = False
                        break
                    
                if exists:
                    break
                
            if not exists:
                FsG[G] = Fk[G]

        return FsG

    def edge_based_join_growth(self,g, minsup):
        ES = get_all_edge_supports(g)
        Fk = self.get_frequent_singleton_graphs_EB(ES, minsup)
        k = 1
    
        FsG = Fk
        C = []
    
        while(True):
            C = self.generate_candidates_EB(list(Fk.keys()), k+1)
            Fk = self.generate_Fkplus1_EB(C, g, minsup)
        
            if not Fk:
                break
        
            FsG = self.update_FsG_EB(Fk, FsG)
            k = k + 1
        
        return FsG
    
"""
Set-up methods
"""



# return list of graphs
def get_graph_database():
    G1 = snap.LoadEdgeList(snap.TUNGraph, "src/datasets/test-graphs/graph-A.txt", 0, 1)
    G2 = snap.LoadEdgeList(snap.TUNGraph, "src/datasets/test-graphs/graph-B.txt", 0, 1)
    G3 = snap.LoadEdgeList(snap.TUNGraph, "src/datasets/test-graphs/graph-C.txt", 0, 1)
    G4 = snap.LoadEdgeList(snap.TUNGraph, "src/datasets/test-graphs/graph-D.txt", 0, 1)
    graph_database = [G1, G2, G3, G4]   
    
    return graph_database


'''
NOTE: (get_all_node_supports) 
This method assumes that there are no label repitions in any of the graphs.
That is, none of the graphs have more than one node with ID x.
'''
# return dict with all nodes in g and their support
def get_all_node_supports(graph_database):
    NS = {}
    
    for graph in graph_database:
        for N in graph.Nodes():
            curr_node = N.GetId()
            if curr_node in NS:
                NS[curr_node] += 1
            else:
                NS[curr_node] = 1
    
    return NS

    
'''
NOTE: (get_all_edge_supports)
This method takes duplication into account.
That is, the edges NodeX-NodeY and NodeY-NodeX are considered the same.
''' 
# return dict will all edges in g and their supports
def get_all_edge_supports(graph_database):
        ES = {}
        
        for graph in graph_database:
            for E in graph.Edges():
                curr_edge = (E.GetSrcNId(), E.GetDstNId())
                curr_edge_flip = (E.GetDstNId(), E.GetSrcNId)
                if curr_edge in ES:
                    ES[curr_edge] += 1
                elif curr_edge_flip in ES:
                    ES[curr_edge_flip] += 1
                else:    
                    ES[curr_edge] = 1
        
        return ES 
    
    
# return all graph edges as list
def graph_to_list(graph):
    graph_list = []
    
    if graph.GetEdges() == 0:
        for N in graph.Nodes():
            graph_list.append(N.GetId())
    else:
        for E in graph.Edges():
            curr_edge = (E.GetSrcNId(), E.GetDstNId())
            graph_list.append(curr_edge)
    
    return graph_list
         
    
# print graphs and their supports / print dict
def print_dict(D, opt):
    if opt == "graph":
        for graph in D.keys():
            print("Graph: {}, Support: {}".format(graph_to_list(graph), D[graph]))
        
    else:
        for key in D.keys():
            print("Key : {} , Value : {}".format(key, D[key]))


# FsG_EB = Frequent subgraphs
# minsup = minimum support


FsG_EB = edgeBased()
# Skaramoosh
print("FsG: ")
print_dict(FsG_EB, "graph")
print("Total: {}".format(len(FsG_EB)))

