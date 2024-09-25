# 20240711
from modules.edge_drivers import *

def multithreading(lst_source_lists:list, def_def:Callable, num_threads:int):
    splitted_lists = split_list(lst_source_lists, num_threads)
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # executor.map(def_def, sources)
        futures = [executor.submit(def_def, lst_sublist) for lst_sublist in splitted_lists]
        for future in futures:
            future.result()
int_threads=3

def wrapper_thread_init_drivers(sublist):
    from types import SimpleNamespace
    global dic_drivers
    dic_drivers[SimpleNamespace()] = None

multithreading(range(int_threads), wrapper_thread_init_drivers, int_threads)


def hi(i,j):
    print(i, j)

# List of names
total = 0
lst_names = ["A", "B", "C", "D", "E"]
# Call the function to greet names concurrently
multithreading(lst_names, hi, 2)


from types import SimpleNamespace
tt={}
a=SimpleNamespace()
tt[a]=1

class HashableObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    def __eq__(self, other):
        if isinstance(other, HashableObject):
            return self.__dict__ == other.__dict__
        return False