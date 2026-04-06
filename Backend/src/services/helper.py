#TODO: Need to correct all function location as some function are causing circular dependency
#NOTE: we kept it here to solve circular dependency as util and curd file where causing circular dependency
def tuple_of_list_to_list(list_is):
    res = [list_is[i][0] for i in range(len(list_is))]
    print(res)
    return res
