def final_a(full_arr, arr):
    first, last = arr
    result = []
    invert = False
    for i in full_arr:
        if i == first:
            invert = True
            
        if invert:
            result.append(-abs(i))
            # result.append(-i)
        else:
            result.append(i)
            
        if i == last and invert:
            invert = False
    return result
            
            
            
print(final_a([1,2,3], [1,3]))