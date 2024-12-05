# treasure.py
class Treasure:
    '''
    Class to implement a treasure
    '''
    
    def __init__(self, id, size, arrival_time):
        '''
        Arguments:
            id : int : The id of the treasure (unique positive integer for each treasure)
            size : int : The size of the treasure (positive integer)
            arrival_time : int : The arrival time of the treasure (non-negative integer)
        Returns:
            None
        Description:
            Initializes the treasure
        '''
        
        # DO NOT EDIT THE __init__ method
        self.id = id
        self.size = size
        self.arrival_time = arrival_time
        self.left_size = size
        self.completion_time = None
    
    # You can add more methods if required




class CrewMate:
    def __init__(self):
        '''
        Initializes a crewmate with an empty heap for treasures and zero load.
        '''
        self.treasures = Heap(
            lambda t1, t2: (t1.arrival_time + t1.left_size) <= (t2.arrival_time + t2.left_size), 
            []
        )
        self.completed_treasures = []  # Store completed treasures here
        self.load = 0
        self.last_update_time = 0  # Tracks the last time the crewmate's load was updated

    def add_treasure(self, treasure):
        '''
        Adds a treasure to the crewmate's heap and updates the load.
        Time complexity: O(log n), where n is the number of treasures in the crewmate's heap
        '''
        time_passed = treasure.arrival_time - self.last_update_time

        # Process all treasures that can be completed in the time that has passed
        while not self.treasures.isempty() and self.treasures.top().left_size <= time_passed:
            top_treasure = self.treasures.extract()
            time_passed -= top_treasure.left_size
            top_treasure.completion_time = treasure.arrival_time - time_passed
            self.completed_treasures.append((top_treasure.id, top_treasure.completion_time))

        # Update remaining load for the top treasure if it hasn't been fully processed
        if not self.treasures.isempty():
            self.treasures.top().left_size -= time_passed

        # Insert the new treasure into the heap and update the load
        self.treasures.insert(treasure)
        self.load += treasure.size
        self.last_update_time = treasure.arrival_time

    def process_remaining_treasures(self):
        '''
        Processes any remaining treasures that haven't been completed yet.
        '''
        time = self.last_update_time
        while not self.treasures.isempty():
            treasure = self.treasures.extract()
            treasure.completion_time = time + treasure.left_size
            self.completed_treasures.append((treasure.id, treasure.completion_time))
            time = treasure.completion_time


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
        # Extract the least-loaded crewmate from the heap
        crewmate = self.heap.extract()
        crewmate.add_treasure(treasure)

        # Reinsert the updated crewmate back into the heap
        self.heap.insert(crewmate)

    def get_completion_time(self):
        '''
        Returns the list of treasures in order of their ids after processing.
        Time complexity: O(n log n), where n is the number of treasures
        '''
        list_treasures = []
        
        # Process any remaining treasures for all crewmates
        for crewmate in self.crewmates:
            crewmate.process_remaining_treasures()
            list_treasures.extend(crewmate.completed_treasures)

        return sorted(list_treasures, key=lambda x: x[0])


# heap.py
class Heap:
    def __init__(self, comparison_function, init_array=[]):
        '''
        Initializes the heap with a comparison function and an initial array.
        Time complexity: O(n), where n is the size of init_array
        '''
        self.comparison_function = comparison_function
        self.heap = init_array[:]
        # Build the heap from the initial array
        for i in range(len(self.heap) // 2, -1, -1):
            self._heapify_down(i)

    def _heapify_down(self, idx):
        '''
        Maintains the heap property from the node at index idx downwards.
        Time complexity: O(log n)
        '''
        left, right = 2 * idx + 1, 2 * idx + 2
        smallest = idx
        if left < len(self.heap) and self.comparison_function(self.heap[left], self.heap[smallest]):
            smallest = left
        if right < len(self.heap) and self.comparison_function(self.heap[right], self.heap[smallest]):
            smallest = right
        if smallest != idx:
            self.heap[smallest], self.heap[idx] = self.heap[idx], self.heap[smallest]
            self._heapify_down(smallest)

    def _heapify_up(self, idx):
        '''
        Maintains the heap property from the node at index idx upwards.
        Time complexity: O(log n)
        '''
        parent = (idx - 1) // 2
        if idx > 0 and self.comparison_function(self.heap[idx], self.heap[parent]):
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            self._heapify_up(parent)

    def insert(self, value):
        '''
        Inserts a value into the heap.
        Time complexity: O(log n), where n is the number of elements currently in the heap
        '''
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def extract(self):
        '''
        Extracts and returns the top value from the heap.
        Time complexity: O(log n)
        '''
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        top_value = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return top_value

    def top(self):
        '''
        Returns the top value from the heap without removing it.
        Time complexity: O(1)
        '''
        return self.heap[0] if self.heap else None
    
    def isempty(self):
        '''
        Returns True if heap is empty, False otherwise.
        Time complexity: O(1)
        '''
        return len(self.heap) == 0

