#!/usr/bin/env python
# coding: utf-8

# # Group 4 - Final Project
# 
# ## _Mining Frequent Subgraphs_
# Harris Mahmood Khawar, Paul Jackson, Drake Kufwafwa, Henry Fox-Jurkowitz  
# _COSC-254: Data Mining_  
# Professor Matteo Riondato 
# 
# 

# NOTE: This project is currently using only test datasets created by us.  
# The file: ```test-graph-desc.pdf``` contains information about the test datasets.
# 
# Please find the ```Main``` cell to see results.

# ## Setup Methods:

# In[ ]:


import snap
import glob
import itertools
import time
import sys
import argparse


# return list of graphs in given directory
def get_graph_database(dir_path):
    graph_paths = glob.glob(dir_path)
    graph_database = []
    
    for path in graph_paths:
        graph_database.append(snap.LoadEdgeList(snap.TUNGraph, path, 0, 1))
    
    return graph_database


#returns list of randomly generated undirected graphs
def get_random_graph_database(numEdges, numNodes, numGraphs):
    graph_database=[]

    for i in range(numGraphs):
        graph_database.append(snap.GenRndGnm(snap.TUNGraph, numNodes, numEdges, False))        
    
    return graph_database


# return all graph edges as list
def list_graph(graph):
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
            print("Graph: {}, Support: {}".format(list_graph(graph), D[graph]))    
    else:
        for key in D.keys():
            print("Key : {} , Value : {}".format(key, D[key]))

# return true if given graphs are the same
def compare_graphs(G1, G2):
    
    if G1.GetNodes() != G2.GetNodes() or G1.GetEdges() != G2.GetEdges(): 
        return False
    
    for N in G1.Nodes():
        if not G2.IsNode(N.GetId()): return False
    
    for E in G1.Edges():
        if not G2.IsEdge(E.GetSrcNId(), E.GetDstNId()): return False
        
    return True   


# Node-based Join Growth:

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


# return dict with frequent singleton graphs and their supports
def get_frequent_singleton_graphs(NS, minsup):
    F1 = {}
    
    for N in NS:
        if NS[N] >= minsup:
            subgraph = snap.TUNGraph.New() # create new graph
            subgraph.AddNode(N) # add frequent node
            F1[subgraph] = NS[N] # graph support = node support
    
    return F1


# return candidate by joining singletons
def join_singletons(subgraph1, subgraph2):
    c = snap.TUNGraph.New() # new candidate subgraph
    c = snap.ConvertGraph(type(subgraph1), subgraph1)
    
    c.AddNode(subgraph2.BegNI().GetId()) # add subgraph2 node to subgraph1
    c.AddEdge(subgraph1.BegNI().GetId(), subgraph2.BegNI().GetId()) # add edge between nodes
        
    return c

'''
NOTE: (subgraph_match)
The book recommends Ullman's Algorithm for this,
which is recursive. I am not a fan recursion so I made the following,
which might not be as efficient but does the job.
'''
# return node and edge if they are the only non-matching ones
def subgraph_match(Gq, G):
    nmE_f = False # non-matching node found
    nmN_f = False # non-matching edge found
    nmN = None # non_matching node
    nmE = None # non-matching edge

    res = False

    for E in Gq.Edges():
        if not G.IsEdge(E.GetSrcNId(), E.GetDstNId()):
            if nmE_f:
                nmE_f = False
                break
            else:
                nmE = (E.GetSrcNId(), E.GetDstNId())
                nmE_f = True
    
    if nmE_f:
        for N in Gq.Nodes():
            if not G.IsNode(N.GetId()):
                if nmN_f:
                    nmN_f = False
                    break
                else:
                    nmN = N.GetId()
                    if nmN in nmE:
                        nmN_f = True
                    else:
                        break
                        
    if nmN_f and nmE_f:
        res = True
    
    return res, nmE, nmN


# return candidates by performing node-based joins    
def join_subgraphs(subgraph1, subgraph2, nmE, nmN):
    
    # create new candidate subgraphs
    c1 = snap.TUNGraph.New()
    c2 = snap.TUNGraph.New()
    
    # hold non-matching node in subgraph2
    for N in subgraph2.Nodes():
        if not subgraph1.IsNode(N.GetId()):
            nmN_s2 = N.GetId()
    
    c1 = snap.ConvertGraph(type(subgraph2), subgraph2) # copy subgraph1
    c1.AddNode(nmN) # add non-matching node from subgraph1
    c1.AddEdge(nmE[0], nmE[1]) # add non-matching edge
    
    c2 = snap.ConvertGraph(type(c1), c1) # copy candidate 1
    c2.AddEdge(nmN, nmN_s2) # add edge between non-matching nodes of subgraph1 and subgraph2
    
    return c1, c2

# return true if all k-1 subgraphs of candidate are in Fk
def prune_candidate(c, Fk, k):
    all_edges = []
    
    for E in c.Edges():
        all_edges.append((E.GetSrcNId(), E.GetDstNId()))
    
    # generate all edges subsets
    kMinus1_subsets = list(itertools.combinations(all_edges, k-2))
    
    for subset in kMinus1_subsets:
        sG = snap.TUNGraph.New()
        exists = False
        
        for tup in subset:
            for N in tup:
                if not sG.IsNode(N): sG.AddNode(N)
            sG.AddEdge(tup[0], tup[1])
        
        if sG.GetNodes() < k: 
            for graph in Fk:
                if compare_graphs(graph, sG):
                    exists = True
                    break

            if not exists:
                return False
        
    return True 

'''
NOTE: (generate_candidates)
This method is incomplete i.e. no optimization/pruning of candidates
'''
# return candidates list by joining graphs in Fk
def generate_candidates(Fk, k):
    candidates = []
    
    for i in range(0, len(Fk)):
        sG1 = Fk[i]
        
        for j in range(i+1, len(Fk)):
            sG2 = Fk[j]
            
            # if graphs are from F1, simply join them
            if k == 2:
                c = join_singletons(sG1, sG2)
                candidates.append(c)
            
            # if graphs are from Fk where k > 1,
            else:
                # join if they each have only one uncommon node
                match, nmE, nmN = subgraph_match(sG1, sG2)
                if match:
                    c1, c2 = join_subgraphs(sG1, sG2, nmE, nmN)
                    for _c in c1, c2:
                        if prune_candidate(_c, Fk, k):
                            candidates.append(_c)
    
    return candidates
        
    
# generate frequent k+1 sized graphs dict by counting C in g
def generate_Fkplus1(C, g, minsup):
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


'''
NOTE: (update_FsG)
This method is not optimized because it is not necessary.
But it is used because if there cycles in the graphs,
duplicate entries are appended to FsG
'''
# return FsG after appending subgraphs not in FsG from Fk
def update_FsG(Fk, FsG):
    exists = False
    
    # compare each graph in Fk with each graph in FsG
    for g in Fk.keys(): 
        
        for G in FsG.keys():
            
            if compare_graphs(g, G):
                exists = True
                
        if not exists:
            FsG[g] = Fk[g]
            
        exists = False
        
    return FsG


# return dict with frequent subgraphs and support
def node_based_join_growth(g, minsup):
    t0 = time.time()
    # NS = { [(NodeId) : Support] }
    NS = get_all_node_supports(g)
    t1 = time.time()
    print("Time for node support count: {:.3f}".format(t1-t0))
    
    # F1 = { All frequent singleton graphs }
    Fk = get_frequent_singleton_graphs(NS, minsup) # frequent k subgraphs
    k = 1
    
    FsG = {} # all frequent subgraphs
    C = [] # candidates from Fk
    
    # Apriori Algorithm:
    while(True):
        print("Run no. : ", k)
        t0 = time.time()
        C = generate_candidates(list(Fk.keys()), k+1)
        t1 = time.time()
        print("Time for candidate generation: {:.3f}".format(t1-t0))
        
        t0 = time.time()
        Fk = generate_Fkplus1(C, g, minsup)
        t1 = time.time()
        print("Time for Fkplus1 generation: {:.3f}".format(t1-t0))
        # end if no more frequent subgraphs
        if not Fk: 
            break
        
        t0 = time.time()
        FsG = update_FsG(Fk, FsG) # append all frequent subgraphs
        t1 = time.time()
        print("Time for update_FsG: {:.3f}".format(t1-t0))
        
        k = k + 1
    
    return FsG


# ## Edge-based Join Growth:

'''
NOTE: (get_all_edge_supports)
This method takes duplication into account.
That is, the edges NodeX-NodeY and NodeY-NodeX are considered the same.
''' 
# return dict will all edges in graph database and their supports
def get_all_edge_supports(graph_database):
        ES = {}    
        
        for graph in graph_database:
            for E in graph.Edges():
                curr_edge = (E.GetSrcNId(), E.GetDstNId())
                curr_edge_flip = (E.GetDstNId(), E.GetSrcNId())
                if curr_edge in ES:
                    ES[curr_edge] += 1
                elif curr_edge_flip in ES:
                    ES[curr_edge_flip] += 1
                else:    
                    ES[curr_edge] = 1
        
        return ES


# return all edges that have at least minsup support   
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


'''
NOTE: (subgraph_match_EB)
The book recommends Ullman's Algorithm for this,
which is recursive. I am not a fan recursion so I made the following,
which might not be as efficient but does the job.
'''
# return node and edge if they are the only non-matching ones
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
            return True, nmE, None
        elif sG2.IsNode(nmE[0]):
            return True, nmE, nmE[1]
        elif sG2.IsNode(nmE[1]):
            return True, nmE, nmE[0]
    
    return False, None, None
    

# return candidates by performing node-based joins        
def join_subgraphs_EB(subgraph1, subgraph2, nmE, nmN):
    
    c = snap.ConvertGraph(type(subgraph2), subgraph2)

    if nmN is not None:
        c.AddNode(nmN)

    c.AddEdge(nmE[0], nmE[1])
    
    return c


# return true if all k-1 subgraphs of candidate are in Fk
def prune_candidate_EB(c, Fk, k):
    all_edges = []
    
    for E in c.Edges():
        all_edges.append((E.GetSrcNId(), E.GetDstNId()))
    
    # generate all edges subsets
    kMinus1_subsets = list(itertools.combinations(all_edges, len(all_edges)-1))

    for subset in kMinus1_subsets:
        sG = snap.TUNGraph.New()
        exists = False
        
        for tup in subset:
            for N in tup:
                if not sG.IsNode(N): sG.AddNode(N)
            sG.AddEdge(tup[0], tup[1])
        
        if sG.GetNodes() <= len(all_edges):
            for graph in Fk:
                if compare_graphs(graph, sG):
                    exists = True
                    break

            if not exists:
                return False
        
    return True 
       
    
# return candidates list by joining graphs in Fk
def generate_candidates_EB(Fk, k):
    candidates = []
    
    for i in range(0, len(Fk)):
        sG1 = Fk[i]
        
        for j in range(i+1, len(Fk)):
            sG2 = Fk[j]
            match, nmE, nmN = subgraph_match_EB(sG1, sG2)
            if match:
                c = join_subgraphs_EB(sG1, sG2, nmE, nmN)
                if prune_candidate_EB(c, Fk, k):
                    candidates.append(c)
                
    return candidates


# generate frequent k+1 sized graphs dict by counting C in g
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


'''
NOTE: (update_FsG)
This method is not optimized because it is not necessary.
But it is used because if there cycles in the graphs,
duplicate entries are appended to FsG
'''
# return FsG after appending subgraphs not in FsG from Fk
def update_FsG_EB(Fk, FsG):
    exists = False

    for g in Fk.keys(): 
        for G in FsG.keys():
            
            if compare_graphs(g, G):
                exists = True
                
        if not exists:
            FsG[g] = Fk[g]
            
        exists = False
        
    return FsG


# return dict with frequent subgraphs and support
def edge_based_join_growth(g, minsup):
    
    # ES = { [ [(SrcNodeId), (DstNodeId) : Support] }
    ES = get_all_edge_supports(g)

    # F1 = { All frequent singleton graphs }
    Fk = get_frequent_singleton_graphs_EB(ES, minsup)
    k = 1
    
    FsG = Fk # all frequent subgraphs
    C = [] # candidates from Fk
    
    # Apriori Algotithm
    while(True):
        C = generate_candidates_EB(list(Fk.keys()), k+1)
        Fk = generate_Fkplus1_EB(C, g, minsup)
        
        # end if no more frequent subgraphs
        if not Fk:
            break
        FsG = update_FsG_EB(Fk, FsG) # append all frequent subgraphs
        
        k = k + 1
        
    return FsG


# ## Main:
usage_info = "USAGE: freq-subgraph-mining.py [-h] -n/-e ([-r], [numNodes, numEdges, numGraphs])/[directory path]\n
[-h]: display usage info\n
[-n]: flag node-based algorithm\n
[-e]: edge-based algorithm\n
[-r]: generate random graphs\n
if [-r]: numNodes, numEdges, numGraphs in random graphdatabase\n
[directory path]: path containing text files for input graphs"




if args.h:
    print(usage_info)
    quit()
    
if args.r:
    if numNodes > 0 and numEdges > 0 and numGraphs > 0: 
        g = get_random_graph_database(numNodes, numEdges, numGraphs)
    else:
        print(usage_info)
elif args

# minsup = minimum support
minsup = 5

# g = [G1, G2, G3 ... Gn] 



# FsG = Frequent subgraphs (with Node-based Join Growth)
FsG = node_based_join_growth(g, minsup)

# Print Results
print_dict(FsG, "graph")
print("Total: ", len(FsG))


# FsG_EB = Frequent subgraphs (with Edge-based Join Growth)
FsG_EB = edge_based_join_growth(g, minsup)

# Print Results
print_dict(FsG_EB, "graph")
print("Total: ", len(FsG_EB))


