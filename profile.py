import settings

# ODN = [
#         [[0,3,1]],
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         [[0,3,1]],
#     ]

def OD_N_per_second(O, D, N, T):
    res = [ [[O, D, N]] for _ in range(T)]
    return res 

def OD_N_per_second_wait_100(O, D, N, T):
    res = [ None for _ in range(T)]
    for i in range(T-100):
        res[i] = [[O, D, N]]
    return res 

def OD_per_20_second(O, D, x, T):
    res = [None for _ in range(T)]
    for i in range(T):
        if i*x % 20 < x/2:
            res[i] = [[O, D, 1]]
    return res

def OD_per_20_second_wait_200(O, D, x, T):
    res = [None for _ in range(T)]
    for i in range(T-200):
        if i*x % 20 < x/2:
            res[i] = [[O, D, 1]]
    return res

def get_ODN(T):
    return OD_per_20_second(0, 3, 10, T)
    # return OD_per_20_second_wait_200(0, 3, 20, T)




