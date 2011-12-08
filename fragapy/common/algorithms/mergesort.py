'''
Created on 1.12.2011

@author: xaralis
'''

def mergesort(l, m, key=lambda e: e):
    """
    Simple implementation of merge sort algorithm to merge two sorted lists
    together comparing same 
    """
    result = []
    i = j = 0
    total = len(l) + len(m)
    
    while len(result) != total:
        if len(l) == i:
            result += m[j:]
            break
        elif len(m) == j:
            result += l[i:]
            break
        elif key(l[i]) < key(m[j]):
            result.append(l[i])
            i += 1
        else:
            result.append(m[j])
            j += 1
    return result