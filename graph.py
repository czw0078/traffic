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

        self.caculate_route() # recaculate later

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

    def rule(self):
        self.caculate_route()

    def go(self):
        pass

