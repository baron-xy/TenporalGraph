import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

'''
Input:
    graphName: name of the graph, including hiv (not yet published), patent, citation-pos, synth_BA, synth_SIR.
    edgeOpt: whether to build direct or undirect graph
    yearStep: # of output_years between two releases
Output:
  Gs: a list of graphs, where Gs[i] represents the graph in output_years[i]
  edis: a list of edi, where edis[i] represents edis of nodes in output_years[i]
  ordered_edges: edges ordered by time
'''

def generate_graphs(graphName, edgeOpt, yearStep=1):
  if graphName in ['hiv','patent','citation-pos']: # read from file hiv/patent
    if graphName == 'hiv':
      raise ValueError('The HIV data is not yet made public.')
      # dataFolder = 'data/hiv'
      # output_years = list(range(1995, 2016+1, yearStep))
    elif graphName == 'patent':
      dataFolder = 'data/patent/'
      output_years = list(range(1985, 1999+1, yearStep))
    else: # graphName == 'citation-pos':
      dataFolder = 'data/citation-pos/'
      output_years = list(range(1990, 2013+1, yearStep))

    Gs, edis, ordered_edges = readGraph_evolvingGraphs(output_years, edgeOpt, dataFolder)

  elif graphName == 'synth_BA': # synthetic Barabasi-Albert graph
    p = 0.5
    m = 1
    num_initial = 500
    num_nodes_per_year = 70
    num_years = 20
    decayOpt = 2
    decay = 1
    output_years = list(range(1, num_years+1, yearStep)) # graph <= year_break(i) is output
    #生成对应的合成图
    # Gs, edis, ordered_edges = BAGraph_evolvingGraphs(p, m, num_years, num_nodes_per_year, num_initial, output_years, edgeOpt, decayOpt, decay)
    # Gs = Gs[1:]
  elif graphName == 'synth_SIR': # synthetic graph w/ SIR model
    perct_initial = 0.05
    rate_transmit = 0.18
    rate_recover = 0.1
    num_years = 20
    output_years = list(range(1, num_years+1, yearStep))
    #生成对应的合成图
    #G, _, _ = BAGraph_evolvingGraphs(0, 2, 1, 5000, 5000, [1], 'undirected', 0, -1) # generate an interaction network with the Barabasi-Albert model
    #Gs, edis, ordered_edges = sir_evolvingGraphs(G[0], perct_initial, rate_transmit, rate_recover, num_years, output_years, edgeOpt)

  else:
    raise ValueError("generate_graphs gets invalid input.")

  return Gs, edis, ordered_edges


