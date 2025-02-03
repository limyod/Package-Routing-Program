
# open probing and chaining were both considered. 
# In a packaging system, where the number of packages may change over time,
# we have decided to use chaining as it handles growth better.
# other considerations: use tree like structure to make look up for chained buckets faster.
class HashTable:
    """class to store key value pairs. no duplicate keys are allowed"""
    def __init__(self, size= 100):
        self.buckets = [None] * size
        self.size = size
        self.elements = 0
        self.LOAD_FACTOR = 0.7

    def _hash(self, key):
        return hash(key) % self.size
    
    def set(self, key, value):
        """sets a key value pair into a hashtable"""
        index = self._hash(key)
        if self.buckets[index] is None:
            #There are no collisions, we can directly insert a listNode
            self.buckets[index] = ListNode(key, value)
            self.elements+=1
        else:
            # There are pre existing elements, lets move our recent element to the top, 
            # assuming recent additions are more likely to be used again
            curr = self.buckets[index]
            while curr is not None:
                if(curr.key == key):
                    curr.value = value
                    return
                curr = curr.next
            # if key is not found..... we should add the pair
            self.buckets[index] = ListNode(key, value, self.buckets[index])
            self.elements+=1
            # resize/rehash if our array is getting full.
            if self.elements / self.size > self.LOAD_FACTOR:
                self._resize(self.size * 2)

    def contains_key(self, key):
        """checks if the hashtable contains the key"""
        index = self._hash(key)
        if self.buckets[index] is None:
            return False
        curr = self.buckets[index]
        while curr is not None:
            if curr.key == key:
                return True
        return False


    def remove(self, key):
        """
        removes the k,v pair of the specified key.
        if the key value pair does not exist, a keyError will be raised
        """
        index = self._hash(key)
        if self.buckets[index] is None:
            raise KeyError(f"Key '{key}' not found in hashSet")
        #edge case for head
        if self.buckets[index].key == key:
            self.buckets[index] = self.buckets[index].next
            self.elements -= 1
            return
        curr = self.buckets[index]
        while curr.next is not None:
            if curr.next.key == key:
                curr.next = curr.next.next
                self.elements -= 1
                return
        raise KeyError(f"Key '{key}' not found in hashSet")

    def get(self, key):
        """
        get the value that corresponds to the key from the hashtable
        raise a keyError if the key doesn't exist
        """
        index = self._hash(key)
        if self.buckets[index] is None :
            return False
        curr = self.buckets[index]
        while curr is not None:
            if curr.key == key:
                return curr.value
        raise KeyError(f"Key '{key}' not found in hashSet")
    
    def _resize(self, size):
        self.size = size
        old_bucket = self.buckets
        self.buckets = [None] * self.size
        for bucket in old_bucket:
            curr = bucket
            while curr is not None:
                self.set(curr.key, curr.value)
                curr = curr.next

class ListNode:
    """
    A simple Node class for implementing a linkedlist within the bucket
    """
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node
