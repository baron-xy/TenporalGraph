'''
Read real graphs from given directory.

Input:
  output_years: when we need to release the statisticas of a graph. 0 for releasing every year; 1 for releasing in the end; any list for specific output_years
  edgeOpt: whether to build direct or undirect graph
  folder: directory where the data lies (assuming 3 files in the directory: 'edges.txt' contain all edges, 'nodes.txt' contains all nodes, 'edis.txt' contains all edis of all nodes)
Output:
  Gs: a list of graphs, where Gs[i] represents the graph in output_years[i]
  edis: a list of edi, where edis[i] represents edis of nodes in output_years[i]
  ordered_edges: edges ordered by time
'''

from rearrangeNodes import *
import networkx as nx

def readGraph_evolvingGraphs(output_years, edgeOpt, folder):
  with open(folder + 'edges.txt') as f:
    edges = [map(int, _.split(',')) for _ in f.read().splitlines()]
  with open(folder + 'nodes.txt') as f:
    nodes = [int(_) for _ in f.read().splitlines()]
  with open(folder + 'edis.txt') as f:
    edis = [int(_) for _ in f.read().splitlines()]

  if (max(nodes) + 1 != len(nodes)) or not all(nodes[i] <= nodes[i+1] for i in range(len(nodes)-1)):
    # print('Nodes are not in [n] or not sorted according to time. Rearrange.')
    nodes, edges, edis = rearrangeNodes(nodes, edges, edis)

  if len(output_years) == 1:
    if output_years == 0: # release every year
      output_years = sorted(list(set(edis)))[1:]
    elif output_years == 1: # release once
      output_years = [max(edis)]
    else:
      print('Wrong value of output_years.')

  nodesets = []
  Gs = []
  adjs = []
  num_nodes = []

  _, edges, edis = rearrangeNodes(nodes, edges, edis)

  ordered_edges = []
  num_edges = len(edges)
  old_edges = [False] * num_edges
  for i_y in range(len(output_years)):
    year = output_years[i_y]
    cur_edges = [(edis[edges[i][0]] <= year) and (edis[edges[i][1]] <= year) for i in xrange(num_edges)]

    ordered_edges += [edges[i] for i in xrange(num_edges) if cur_edges[i] and not old_edges[i]]
    old_edges = cur_edges

    nodesets.append([node for node in nodes if edis[node] <= year])
    num_nodes.append(len(nodesets[-1]))

    if edgeOpt == 'undirected':
      Gs.append(nx.Graph())
    else:
      Gs.append(nx.DiGraph())
    Gs[-1].add_nodes_from(nodesets[-1])
    Gs[-1].add_edges_from([edges[i] for i in range(len(cur_edges)) if cur_edges[i]])

  return Gs, edis, ordered_edges