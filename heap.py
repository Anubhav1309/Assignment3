class Heap:
    def __init__(self, comparison_function, init_array=[]):
        '''
        Initializes the heap with a comparison function and an initial array.
        Time complexity: O(n), where n is the size of init_array
        '''
        self.comparison_function = comparison_function
        self.heap = init_array[:]
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