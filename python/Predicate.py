s = [1, 2, 3, 4, 5]
p = lambda x: x > 2
# def for_All(p,s):
#     for x in s:
#         if not p in s:
#             return False
#     return True

# print(for_All(p,s))

def for_Some(p,s):
    for element in s:
        if p(element):
            return True
    False

print(for_Some)

forsome= lambda p,s : len([*filter(p,s)])
