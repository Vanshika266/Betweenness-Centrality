import re
import itertools

class Graph(object):

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges
        
        access=[]
        p=0
        while p<len(self.edges):
            access.append(self.edges[p])
            access.append((self.edges[p][1],self.edges[p][0]))
            p=p+1
        self.access=access
            
        f=0
        neighbour=[]
        while f<len(self.vertices):
            g=0
            while g<len(self.access):
                if self.access[g][0]==self.vertices[f]:
                    neighbour.append((self.vertices[f],self.access[g][1]))
                g=g+1
            f=f+1
        self.neighbour = neighbour
        # neighbour is the list which have all neighbours from the graph
                    
        self.validate()
    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''
        # Implementing BFS to find minimum distance between two nodes
        remaining=[]
        verified=[]
        dist=['-']
        remaining.append(start_node)
        while len(remaining) != 0:
            verified.append(remaining[0])
            j=0
            while j<len(self.neighbour):
                if self.neighbour[j][0]==remaining[0]:
                    if self.neighbour[j][1] not in remaining and self.neighbour[j][1] not in verified:
                        remaining.append(self.neighbour[j][1])
                        dist.append(self.neighbour[j])
                j=j+1
            remaining.remove(remaining[0])
        u=1
        check=end_node
        count=0
        while u<len(dist):
            if dist[u][1]==check:
               count=count+1
               if dist[u][0]==start_node:
                   return count
               else:
                   check=dist[u][0]
                   u=0
                
            u=u+1
            


    def all_paths(self,node, destination, dist, path):
        """
        Finds all paths from node to destination with length = dist

        Args:
            node: Node to find path from
            destination: Node to reach
            dist: Allowed distance of path
            path: path already traversed

        Returns:
            List of path, where each path is list ending on destination

            Returns None if there no paths
        """
        path = path + [node]
        if len(path)==int(dist)+1:
            if node == destination:
                return path
            else:
                return None
        final_paths=[]
        r=0
        while r<len(self.neighbour):
            if self.neighbour[r][0]==node:
                if self.neighbour[r][1] not in path:
                    ans=self.all_paths(self.neighbour[r][1],destination,dist,path)
                    if ans is not None:
                        if isinstance(ans[0],list):
                            final_paths=final_paths+ans
                        else:
                            final_paths.append(ans)
            r=r+1
        # final_paths have all paths of distance two between two nodes
        if len(final_paths) != 0:
            return final_paths
        else:
            return None
                                 

    def all_shortest_paths(self,start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """

        distance = self.min_dist(start_node,end_node)
        path = self.all_paths(start_node,end_node,distance,[])
        return path

    def betweenness_centrality(self, node):
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """
        np=0
        # node_pairs have all pairs of nodes ( except node )
        node_pairs=[]
        while np<len(self.vertices):
            if self.vertices[np] != node:
                np1=np+1
                while np1<len(self.vertices):
                    if self.vertices[np1] != node and self.vertices[np] != self.vertices[np1]:
                        node_pairs.append([self.vertices[np],self.vertices[np1]])
                    np1=np1+1
            np=np+1
        idx=0
        # shortest list have the count of number of shortest paths between two nodes ( parallel with node_pairs )
        shortest=[]
        while idx<len(node_pairs):
            ta=self.all_shortest_paths(node_pairs[idx][0],node_pairs[idx][1])
            shortest.append(len(ta))
            idx=idx+1
        inc=0
        # passing list have the count of shortest paths which goes through node
        passing=[]
        while inc<len(node_pairs):
            sp=self.all_shortest_paths(node_pairs[inc][0],node_pairs[inc][1])
            counter=0
            h=0
            while h<len(sp):
                if node in sp[h]:
                    counter=counter+1
                h=h+1
            passing.append(counter)    
            inc=inc+1
        to_sum=[]
        y=0
        while y<len(passing):
            to_app = passing[y]/shortest[y]
            to_sum.append(to_app)
            y=y+1
        sm=0
        centrality=0
        while sm<len(to_sum):
            centrality=centrality+to_sum[sm]
            sm=sm+1
        # centrality is the betweenness centrality of a node
        lth=len(self.vertices)
        denom= ((lth-1)*(lth-2))/2
        # standard is the Standardized Betweenness Centrality 
        standard= centrality/denom
        return standard
               

    def top_k_betweenness_centrality(self):
        """
        Find top k nodes based on highest equal betweenness centrality.

        
        Returns:
            List a integer, denoting top k nodes based on betweenness
            centrality.
        """

        z=0
        # top_k list have Standardized Betweenness Centrality for nodes
        top_k=[]
        while z<len(self.vertices):
            ans = self.betweenness_centrality(self.vertices[z])
            top_k.append(ans)
            z=z+1
        # compare have the maximum Standardized Betweenness Centrality 
        compare=max(top_k)
        fl=0
        # Final_Answer have all the nodes with maximum Standardized Betweenness Centrality 
        Final_Answer=[]
        while fl<len(top_k):
            if top_k[fl] == compare:
                Final_Answer.append(self.vertices[fl])
            fl=fl+1
        print("Standardized Betweenness Centrality is - ", compare)
        print("k -",len(Final_Answer))
        return Final_Answer
            
            

if __name__ == "__main__":
    vertices = [1, 2, 3, 4, 5, 6]
    edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4),(3, 6), (4, 5), (4, 6)]

    graph = Graph(vertices, edges)
    print("Top k nodes - ",graph.top_k_betweenness_centrality())
