import sys
from sys import argv

def start_simulation(no_of_processor, distribution_type):
    max_memory_module = 2048
    for curr_memory in range (1, max_memory_module):
        print(curr_memory)

if __name__ == "__main__":
    a = sys.argv[0]
    if len(argv) < 3:
        print("Please enter number of processors and distribution type as command line arguments")
    else:
        no_of_processor = argv[1]
        distribution_type = argv[2]
        print("Memory Module", "W_Dash")
        start_simulation(no_of_processor, distribution_type)

