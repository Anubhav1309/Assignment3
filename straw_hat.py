from crewmate import CrewMate
from heap import Heap
from treasure import Treasure

class StrawHatTreasury:
    def __init__(self, m):
        '''
        Initializes the StrawHatTreasury with m crewmates.
        Time complexity: O(m), where m is the number of crewmates
        '''
        self.crewmates = [CrewMate() for _ in range(m)]
        self.heap = Heap(lambda c1, c2: c1.load < c2.load, self.crewmates)

    def add_treasure(self, treasure):
        '''
        Adds a treasure to the least loaded crewmate and updates the current time.
        Time complexity: O(log m + log n), where:
            m is the number of crewmates,
            n is the number of treasures assigned to the selected crewmate
        '''

        u = self.heap.extract()
        u.add_treasure(treasure)
        self.heap.insert(u)

    def get_completion_time(self):
        '''
        Returns the list of treasures in order of their ids after processing.
        Time complexity: O(n log n), where n is the number of treasures
        '''

        list_treasures = []
        for c in self.crewmates:
            t = c.load_t
            r = Heap(lambda t1, t2: (
            (t1.arrival_time + t1.left_size) < (t2.arrival_time + t2.left_size) or
            ((t1.arrival_time + t1.left_size) == (t2.arrival_time + t2.left_size) and t1.id < t2.id)
        ),
        [])

            while c.treasures.isempty() is not True:
                u = c.treasures.extract()
                r.insert(u)
                u.completion_time = t + u.left_size
                temp = Treasure(u.id,u.arrival_time,u.size)
                temp.completion_time = u.completion_time
                list_treasures.append(temp)
                t = u.completion_time

            c.treasures = r
            for x in c.find_ex:
                list_treasures.append(x)
                
        return sorted(list_treasures, key=lambda x: x.id)
