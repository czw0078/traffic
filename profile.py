import settings

# ODN = [
#         [[0,4,1]],
#         None,
#         None,
#         None,
#         None,
#         [[3,4,1]]
#     ]

def OD_per_20_second(O, D, x, T):
    res = [None for _ in range(T)]
    for i in range(T):
        if i*x % 20 < x/2:
            res[i] = [[O, D, 1]]
    return res

def get_ODN(T):
    return OD_per_20_second(0, 3, 1, T)

