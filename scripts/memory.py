import sys
import random
from sys import argv

processor_request = []
processor_access_counter = []
processor_priority = []


def init_processor_array(no_of_processor):
    """
    Initializes three arrays
     1. processor_requests: array that stores the values of memory modules that a particular processor is assigned
     2. processor_access_counter: array to keep count of how many many times a processor has be granted access to its
     memory
     3. processor_priority: array to store the priority of each processor based on which they are granted memory access
    :param no_of_processor: number of processor
    :return: initialize processor priority, request and access counter.
    """
    global processor_request
    global processor_access_counter
    global processor_priority

    processor_request = []
    processor_access_counter = []
    processor_priority = []
    for i in range(0, no_of_processor):
        processor_request.append(0)
        processor_access_counter.append(0)
        processor_priority.append(i)


def generate_random_memory_requests(current_number_memory_cycles):
    return random.randint(1, current_number_memory_cycles)


def generate_memory_requests(no_of_processor, current_memory):
    for i in range(0, no_of_processor):
        processor_request[i] = generate_random_memory_requests(current_memory)


def run_simulation_normal(no_of_processor, curr_memory):
    print("")


def processor_with_highest_priority_for_a_memory(memory_module, no_of_processor):
    """
    :param no_of_processor: Total Number of processors
    :param memory_module: The memory module for which highest priority needs to be found
    :return: The Processor having highest priority for that memory module
    """
    priority_of_processor = 10000
    highest_priority_processor= -1
    for processor in range(0, no_of_processor):
        if processor_request[processor] == memory_module+1:
            if processor_priority[processor] < priority_of_processor:
                priority_of_processor = processor_priority[processor]
                highest_priority_processor = processor
    return highest_priority_processor


def processor_access_counter_has_increased(index):
    if processor_access_counter[index] > processor_access_counter[index-1]:
        return True
    return False


def cycle_priorities():
    global processor_priority
    x = []
    processor_priority = processor_priority[1:] + processor_priority[:1]


def all_processor_paired():
    return 0 not in processor_access_counter


def run_simulation_uniform(no_of_processor, curr_memory):
    generate_memory_requests(no_of_processor, curr_memory)
    max_cycles = 1000
    cycle = 1
    is_w_stable = False
    w0 = 0.0
    w_prev = 0.0
    w_diff = 0.0
    while cycle < max_cycles and not is_w_stable:
        for i in range(0, no_of_processor):
            if processor_access_counter_has_increased(i):
                processor_request[i] = generate_random_memory_requests(curr_memory)
        for memory in range(0, curr_memory):
            processor_with_highest_priority = processor_with_highest_priority_for_a_memory(memory, no_of_processor)
            if processor_with_highest_priority >= 0:
                processor_access_counter[processor_with_highest_priority] = \
                    processor_access_counter[processor_with_highest_priority] + 1
        cycle_priorities()
        cycle = cycle + 1
        if all_processor_paired():
            w_prev = w0
            w0 = calculate_w0(no_of_processor, cycle)
            w_diff = w0 - w_prev
            is_w_stable = check_stability(w_diff, w_prev)
            if is_w_stable:
                print(w0)


def check_stability(w_diff, w_prev):
    if w_diff < w_prev*0.01:
        return True
    else:
        return False


def calculate_w0(no_of_processor, cycle):
    w0 = 0.0
    sum = 0.0
    processor_w = []
    for processor in range(0, no_of_processor):
        w = cycle/processor_access_counter[processor]
        processor_w.append(w)
    for processor in range(0, no_of_processor):
        sum = sum + processor_w[processor]
    w0 = sum/no_of_processor
    return w0


def run_simulation_normal(no_of_processor, curr_memory):
    generate_memory_requests(no_of_processor, curr_memory)
    locality_of_reference_list = []
    locality_of_reference_list = processor_request
    max_cycles = 1000
    cycle = 1
    w0 = 0.0
    w_prev = 0.0
    w_diff = 0.0
    is_w_stable = False
    while cycle < max_cycles and not is_w_stable:
        for i in range(0, no_of_processor):
            if processor_access_counter_has_increased(i):
                memory_requested_normal = int(random.gauss(locality_of_reference_list[i], curr_memory/6))
                if memory_requested_normal > 0:
                    processor_request[i] = memory_requested_normal
                else:
                    processor_request[i] = curr_memory + locality_of_reference_list[i] + memory_requested_normal
                #print("Cycle number is {0} and current Memory Module is {1}".format(cycle, curr_memory))
                #print(processor_request[i])
        for memory in range(0, curr_memory):
            processor_with_highest_priority = processor_with_highest_priority_for_a_memory(memory, no_of_processor)
            if processor_with_highest_priority >= 0:
                processor_access_counter[processor_with_highest_priority] = \
                    processor_access_counter[processor_with_highest_priority] + 1
        cycle_priorities()
        cycle = cycle + 1
        if all_processor_paired():
            w_prev = w0
            w0 = calculate_w0(no_of_processor, cycle)
            w_diff = w0 - w_prev
            is_w_stable = check_stability(w_diff, w_prev)
            if is_w_stable:
                print(w0)


def start_simulation(no_of_processor, distribution_type):
    max_memory_module = 2048
    for curr_memory in range(1, max_memory_module):
        init_processor_array(no_of_processor)
        if distribution_type == 'u':
            run_simulation_uniform(no_of_processor, curr_memory)
        elif distribution_type == 'n':
            run_simulation_normal(no_of_processor, curr_memory)
        else:
            print("Please enter distribution type as either 'u' or 'n'")


if __name__ == "__main__":
    a = sys.argv[0]
    if len(argv) < 2:
        print("Please enter number of processors and distribution type as command line arguments")
    else:
        #no_of_processor = argv[0]
        #distribution_type = argv[1]
        no_of_processor = 128
        distribution_type = 'n'
        start_simulation(no_of_processor, distribution_type)