class A_Star:
    from math import sqrt

    _instances = set()
    _alive = True

    def __init__(self, Map, start_point, destination_point, user):
        from PIL import Image
        import weakref
        self._instances.add(weakref.ref(self))

        self.height_map = []
        self.forbidden_map = []
        self.start_point = start_point
        self.destination_point = destination_point
        self.user = user
        self.map_query = Map

        height_map_data = Image.open(Map.height_map)
        map_size = height_map_data.size
        height_map_data = list(height_map_data.getdata())

        forbidden_map_data = list(Image.open(Map.forbidden_map).getdata())

        for i in range(map_size[1]):
            self.height_map.append(list(map(lambda x: int(x[0]), height_map_data[ i*map_size[0] : (i+1)*map_size[0] ])))
            self.forbidden_map.append(list(map(lambda x: True if (int(x[0]) != 255) or (int(x[1]) != 255) or (int(x[2]) != 255) else False, forbidden_map_data[ i*map_size[0] : (i+1)*map_size[0] ])))

        self.WIDTH = len(self.height_map[0])
        self.HEIGHT = len(self.height_map)
        self.curent_q = None
        
        self.width_meter = Map.width_meter
        self.pixel_to_meter_convert_ratio = self.width_meter/self.WIDTH
        self.height_meter = self.pixel_to_meter_convert_ratio*self.HEIGHT

        # (address, parrent_address, F_cost) -> type of each index of open_list
        # exp -> ((2,1), (1,1), 5)
        self.open_list = []
        self.close_list = []


    @classmethod
    def update_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is None:
                dead.add(ref)
        cls._instances -= dead

    @classmethod
    def kill_instance(cls, thread_address):
        for instance in cls._instances:
            if str(thread_address) in str(instance):
                instance().kill()
                break

    def kill(self):
        self._alive = False

    def _h(self, s):
        sx, sy = s
        dx, dy = self.destination_point
        h = self.sqrt((sx-dx)**2 + (sy-dy)**2)
        return h

    def g(self, point_address, parrent_point):
        return self._calculate_time_of_arrival(self._find_way(point_address, parrent_point[0]))

    def _f(self, point_address, parrent_point):
        return self.g(point_address, parrent_point) + self._h(point_address)

    def _min_f(self):
        min_f = min(self.open_list, key= lambda x: x[2])
        index_min_f = self.open_list.index(min_f)
        res = self.open_list.pop(index_min_f)
        self.close_list.append(res)
        self.curent_q = res
        return res

    def _generate_ways(self, Cell):
        x,y = Cell
        ls = []
        for i in range(-1,2):
            for j in range(-1,2):
                if not((i,j)==(0,0)):
                    ls.append( (x-j, y-i) )
        self._check_way_out_of_border(ls)
        return ls

    def _check_way_out_of_border(self, ways):
        index = 0
        while index < len(ways):
            if not ((ways[index][0] > -1) and (ways[index][0] < self.WIDTH) and (ways[index][1] > -1) and (ways[index][1] < self.HEIGHT)):
                ways.remove(ways[index])
                index -= 1
            elif self.forbidden_map[ways[index][0]][ways[index][1]]:
                ways.remove(ways[index])
                index -= 1
            index += 1

    def _append_best_way(self, temp_open_list):
        for open in temp_open_list:
            temp_open_list_same_point = list(filter(lambda x: x[0]==open[0], self.open_list))
            temp_close_list_same_point = list(filter(lambda x: x[0]==open[0], self.close_list))
            if len(temp_open_list_same_point) > 0:
                temp_open_list_same_point = temp_open_list_same_point[0]
                if temp_open_list_same_point[2] > open[2]:
                    self.open_list.remove(temp_open_list_same_point)
                    self.open_list.append(open)
            elif len(temp_close_list_same_point) == 0:
                self.open_list.append(open)
                
    def _check_arrived(self, ways):
        for way in ways:
            if way == self.destination_point:
                return way
        return False

    def _find_way(self, way, parent):
        res = []
        res.append(way)
        try:
            while True:
                parent = list(filter(lambda x: x[0]==parent, self.close_list))[0]
                res.append(parent[0])
                parent = parent[1]
        except :
            return res[::-1]

    def _calculate_way_distance(self, dir):
        res = 0
        dir_len = len(dir)
        for i in range(dir_len):
            if i+1 == dir_len:
                break
            x1, y1 = dir[i]
            x2, y2 = dir[i+1]
            point_height = self.height_map[x1][y1]
            parent_height = self.height_map[x2][y2]
            distance_xy_pow2 = 2
            if (x1 == x2) | (y1 == y2):
                distance_xy_pow2 = 1
            height_pow2 = abs(point_height - parent_height)**2
            res += self.sqrt(distance_xy_pow2 + height_pow2)
        return res

    def _calculate_2d_distance(self, first, second):
        return(self.sqrt((first[0]-second[0])**2 + (first[1]-second[1])**2))

    def calculate_speed(self, first, second):
        x1, y1 = first
        x2, y2 = second
        side_adjacent = self.sqrt(2) * self.pixel_to_meter_convert_ratio
        if (x1 == x2) or (y1 == y2):
            side_adjacent = 1 * self.pixel_to_meter_convert_ratio
        hypotenuse = self._calculate_way_distance([first, second]) * self.pixel_to_meter_convert_ratio
        f_height = self.height_map[x1][y1]
        s_height = self.height_map[x2][y2]
        return 100 * (side_adjacent / hypotenuse) if f_height < s_height else 100 / (side_adjacent / hypotenuse)

    # t= d/s
    def _calculate_time_of_arrival(self, dir):
        res = 0
        dir_len = len(dir)
        for i in range(dir_len):
            if i+1 >= dir_len:
                break
            res += (self._calculate_way_distance([dir[i], dir[i+1]]) * self.pixel_to_meter_convert_ratio) / self.calculate_speed(dir[i], dir[i+1])
        return res

    def _calculate_time_of_arrival_for_display(self, dir):
        distance = self._calculate_way_distance(dir)*self.pixel_to_meter_convert_ratio
        return distance / 83

    def start(self):
        self.open_list.append((self.start_point , None, 0))
        while (len(self.open_list) > 0) & (self._alive):
            q = self._min_f()
            yield {"done": False, "response": self._find_way(q[0], q[1])}
            ways = self._generate_ways(q[0])
            check_arrived_res = self._check_arrived(ways)
            if check_arrived_res:
                self.res_dir = self._find_way(check_arrived_res, q[0])
                self.res_dir_distance = self._calculate_way_distance(self.res_dir)*self.pixel_to_meter_convert_ratio
                self.res_2d_distance = self._calculate_2d_distance(self.start_point, self.destination_point)*self.pixel_to_meter_convert_ratio
                self.res_time_of_arrival = self._calculate_time_of_arrival_for_display(self.res_dir)
                from website.views import write_history, delete_map_thread
                history_id = write_history(self.user, self.map_query, self.start_point, self.destination_point, self.res_dir, self.res_dir_distance, self.res_2d_distance, self.res_time_of_arrival)
                yield {"done": True, "response": (self.res_2d_distance, self.res_dir_distance, self.res_time_of_arrival)}
                delete_map_thread(str(self).split(' ')[-1][:-1])
            else:
                temp_open_list = []
                for way in ways:
                    temp_open_list.append((way, q[0], self._f(way, q)))
                self._append_best_way(temp_open_list)

    def log(self):
        print(self.res_dir)
        print(self.res_dir_distance)
        print(self.res_2d_distance)
        print(self.res_time_of_arrival)