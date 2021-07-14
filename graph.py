 #!/usr/bin/env python3

class Network:
    def __init__(self, node_list, road_list):
        self.INF = 1000000
        self.node_list = node_list
        self.road_list = road_list
        self.cost = {}
        self.next = {}
        self.n2r = {}
        for a in self.node_list:
            self.cost[a] = {}
            self.next[a] = {}
            self.n2r[a] = {}

        for r in road_list:
            self.n2r[r.start][r.end] = r

    def caculate_route(self):
        for a in self.node_list:
            for b in self.node_list:
                if a == b:
                    self.cost[a][b] = 0
                    self.next[a][b] = b
                else:
                    self.cost[a][b] = self.INF
                    self.next[a][b] = None

        for r in self.road_list:
            self.cost[r.start][r.end] = r.get_travel_time()
            self.next[r.start][r.end] = r.end

        for k in self.node_list:
            for i in self.node_list:
                for j in self.node_list:
                    if self.cost[i][j] > self.cost[i][k]+self.cost[k][j]:
                        self.cost[i][j] = self.cost[i][k] + self.cost[k][j]
                        self.next[i][j] = self.next[i][k]

    def get_path(self, i,j):
        if self.next[i][j] == None:
            return []
        points = [i]
        while i != j:
            i = self.next[i][j]
            points.append(i)

        res = []
        for index in range(len(points) - 1):
            r = self.n2r[points[index]][points[index+1]]
            res.append(r)
        return res

    def get_current_and_next_road(self, i, j):
        if self.next[i][j] == None:
            return None, None
        points = [i]
        n = 0
        while i != j and n < 2:
            i = self.next[i][j]
            points.append(i)
            n += 1
        if len(points) < 2:
            return None, None
        elif len(points) == 2:
            return self.n2r[points[0]][points[1]], None
        elif len(points) == 3:
            return self.n2r[points[0]][points[1]], self.n2r[points[1]][points[2]]

def prepare():
    v0 = Node(0)
    v1 = Node(1)
    v2 = Node(2)
    v3 = Node(3)
    r0 = Road(v0, v1, 5)
    r1 = Road(v0, v3, 7)
    r2 = Road(v1, v2, 4)
    r3 = Road(v1, v3, 2)
    r4 = Road(v2, v0, 3)
    r5 = Road(v2, v1, 3)
    r6 = Road(v2, v3, 2)
    r7 = Road(v3, v2, 1)
    node_list = [v0, v1,v2,v3]
    road_list = [r0, r1,r2,r3,r4,r5,r6,r7]
    network = Network(node_list, road_list)
    network.caculate_route()
    print(network.cost)
    print(network.next)
    print(network.get_path(v1, v0))
    print(network.get_path(v3, v1))
    print(network.get_current_and_next_road(v1, v0))
    print(network.get_current_and_next_road(v3, v1))



