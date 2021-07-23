
# utility function
def OD_per_20_second(O, D, x):
    T = total_ticks
    res = [None for _ in range(T)]
    for i in range(T):
        if i*x % 20 < x/2:
            res[i] = [[O, D, 1]]
    return res

def OD_per_20_second_wait_200(O, D, x):
    T = total_ticks
    res = [None for _ in range(T)]
    for i in range(T-200):
        if i*x % 20 < x/2:
            res[i] = [[O, D, 1]]
    return res

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

# for debug
total_ticks = 400
random_seed = 10 # debug later


def get_ODN(): # O D N
    return OD_per_20_second_wait_200(0, 5, 10)

def prepare_patch_list(obj):
    n0 = obj.node(-404, 55)
    n1 = obj.node(-354, 0)
    n2 = obj.node(-177, 182)
    n3 = obj.node(0, 5)
    n4 = obj.node(177, 182)
    n5 = obj.node(354, 0)

    n6 = obj.node(-177, -182)
    n7 = obj.node(0, -5)
    n8 = obj.node(177, -182)

    r0 = obj.road(n0, n1)
    r1 = obj.road(n1, n2)
    r2 = obj.road(n2, n3)
    r3 = obj.road(n3, n4, v_free=11)
    r4 = obj.road(n4, n5, v_free=11)

    r5 = obj.road(n1, n6, v_free=11)
    r6 = obj.road(n6, n7, v_free=11)
    r7 = obj.road(n7, n8)
    r8 = obj.road(n8, n5)

    # r9 = obj.road(n3, n7)





