'''
Rearrange nodes (and edges and edis) when nodes do not range from 0 to # of nodes - 1
'''

def rearrangeNodes(nodes, edges, edis):
  # if nodes are not in range 0 to n-1, convert them to
  n = len(nodes);
  if max(nodes) != n - 1:
    mapping = {nodes[i]:i for i in range(n)}
    edges = [[mapping[u], mapping[v]] for u, v in edges]

  # sort node according to edi
  nodes = range(n)
  edis = [edis[node] for node in nodes]
  edis, nodes = map(list, zip(*sorted([(edi, i) for i, edi in enumerate(edis)])))  # sort nodes according to edi
  mapping = {nodes[i]:i for i in range(n)} # assign new index for nodes
  edges = [[mapping[u], mapping[v]] for u, v in edges]
  edges.sort()
  nodes = range(n)

  return nodes, edges, edis
