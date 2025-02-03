
# open probing and chaining were both considered. 
# In a packaging system, where the number of packages may change over time,
# we have decided to use chaining as it handles growth better.
# other considerations: use tree like structure to make look up for chained buckets faster.
class HashTable:
    def __init__(self, size= 100):
        self.buckets = [None] * size
        self.size = size
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def insert(self, key, value):
        index = self._hash(key)
        if(self.buckets[index] == None):
            #There are no collisions, we can directly insert a listNode
            self.buckets[index] = ListNode(key, value)
        else:
            # There are pre existing elements, lets move our recent element to the top, 
            # assuming recent additions are more likely to be used again
            self.buckets[index] = ListNode(key, value, self.buckets[index])
        

    def remove(self, key):
    
    def get(self, key):

    def _resize(self, size):


class ListNode:
    def __init__(self, key, value, next=None):
        self.key = key
        self.value = value
        self.next = next
