#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Depth first search algorithm
# Based on http://www.boost.org/doc/libs/1_52_0/libs/graph/doc/depth_first_search.html
#
# Copyright (C) UPMC Paris Universitas
# Authors:
#   Marc-Olivier Buob <marc-olivier.buob@lip6.fr>
#   Jordan Augé       <jordan.auge@lip6.fr> 

class dfs_color:
    WHITE = 1 # not yet visited
    GRAY  = 2 # currently visited
    BLACK = 3 # visited

#DFS(G)
#  for each vertex u in V 
#    color[u] := WHITE
#    p[u] = u 
#  end for
#  time := 0
#  if there is a starting vertex s
#    call DFS-VISIT(G, s)
#  for each vertex u in V 
#    if color[u] = WHITE
#      call DFS-VISIT(G, u)
#  end for
#  return (p,d_time,f_time) 

def dfs(graph, root, exclude_uv=None):
    """
    \brief Run the DFS algorithm
    \param graph The graph we explore
    \param root The starting vertex
    \return A dictionnary which maps each vertex of the tree
            to its predecessor, None otherwise.
            Only the root node as a predecessor equal to None.
            Nodes not referenced in this dictionnary do not
            belong to the tree.
    """
    # Initialization
    map_vertex_color = {}
    map_vertex_pred  = {}
    for u in graph.nodes():
        map_vertex_color[u] = dfs_color.WHITE
        map_vertex_pred[u] = None 

    # Recursive calls
    if not exclude_uv:
        exclude_uv = lambda u,v: False
    dfs_visit(graph, root, map_vertex_color, map_vertex_pred, exclude_uv)

    # Remove from map_vertex_pred the vertices having no
    # predecessor but the root node.
    for v, u in map_vertex_pred.items():
        if u == None and v != root:
            del map_vertex_pred[v]

    return map_vertex_pred

#DFS-VISIT(G, u) 
#  color[u] := GRAY
#  d_time[u] := time := time + 1 
#  for each v in Adj[u] 
#    if (color[v] = WHITE)
#      p[v] = u 
#      call DFS-VISIT(G, v)
#    else if (color[v] = GRAY) 
#      ...
#    else if (color[v] = BLACK) 
#      ...
#  end for
#  color[u] := BLACK
#  f_time[u] := time := time + 1 

def dfs_visit(graph, u, map_vertex_color, map_vertex_pred, exclude_uv):
    """
    \brief Internal usage (DFS implementation) 
    \param graph The graph we explore
    \param u The current node 
    \param map_vertex_color: maps each vertex to a color
        - dfs_color.WHITE: iif the vertex is not reachable from the root node
        - dfs_color.BLACK: otherwise
    \param map_vertex_pred: maps each vertex to its predecessor (if any) visited
        during the DFS exploration, None otherwise
    """
    map_vertex_color[u] = dfs_color.GRAY
    for v in graph.successors(u):
        color_v = map_vertex_color[v]
        if color_v == dfs_color.WHITE and not exclude_uv(u, v):
            map_vertex_pred[v] = u
            dfs_visit(graph, v, map_vertex_color, map_vertex_pred, exclude_uv)
    map_vertex_color[u] = dfs_color.BLACK

