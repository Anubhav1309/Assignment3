from heap import Heap
from treasure import Treasure
class CrewMate:
    def __init__(self):
        '''
        Initializes a crewmate with an empty heap for treasures and zero load.
        '''
        self.treasures = Heap(
            lambda t1, t2: (
            (t1.arrival_time + t1.left_size) < (t2.arrival_time + t2.left_size) or
            ((t1.arrival_time + t1.left_size) == (t2.arrival_time + t2.left_size) and t1.id < t2.id)
        ),
        []
        )
        self.find_ex = []
        self.load = 0
        self.load_t = 0

    def add_treasure(self, treasure):
        '''
        Adds a treasure to the crewmate's heap and updates the load.
        Time complexity: O(log n), where n is the number of treasures in the crewmate's heap
        '''

        t = treasure.arrival_time - self.load_t

        while self.treasures.isempty() is not True:

            u = self.treasures.top()
            if u.left_size <= t:
                j = self.treasures.extract()
                t = t - j.left_size
                j.completion_time = treasure.arrival_time - t
                temp = Treasure(j.id,j.arrival_time,j.size)
                temp.completion_time = j.completion_time
                self.find_ex.append(temp)
            else:
                j = self.treasures.extract()
                j.left_size -= t
                self.treasures.insert(j)
                break
        

        self.load  = max(0,self.load - t)
        self.treasures.insert(treasure)
        self.load += treasure.size
        self.load_t = treasure.arrival_time
        
    def process_treasure(self):
        '''
        Processes the treasure with the highest priority (min-heap top).
        Time complexity: O(log n), where n is the number of treasures in the heap
        '''
        return None