# Python program to print largest contiguous array sum

from sys import maxsize

# Function to find the maximum contiguous subarray
# and print its starting and end index
def maxSubArraySum(a):
    size=len(a)

    max_so_far = -maxsize - 1
    max_ending_here = 0
    start = 0
    end = 0
    s = 0

    for i in range(0,size):

        max_ending_here += a[i]

        if max_so_far < max_ending_here:
            max_so_far = max_ending_here
            start = s
            end = i

        if max_ending_here < 0:
            max_ending_here = 0
            s = i+1






    return max_so_far, start, end

# Driver program to test maxSubArraySum
#a = [-2, -3, 4, -1, -2, 1, 5, -3]
a = [-0.2, -0.3, 0.4, -0.1, -0.2, -0.1, -0.5, -0.3]
max_so_far,start,end=maxSubArraySum(a)

print(max_so_far,start,end)
