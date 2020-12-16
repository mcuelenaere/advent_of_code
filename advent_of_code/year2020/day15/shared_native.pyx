from libc.stdlib cimport calloc, free

def play_memory_game(numbers, Py_ssize_t max_turn):
    cdef Py_ssize_t numbers_length = len(numbers)
    cdef unsigned long *numbers_history = <unsigned long*> calloc(max_turn + 1, sizeof(unsigned long))
    if not numbers_history:
        raise MemoryError()

    cdef unsigned long last_number
    cdef unsigned int turn, i
    try:
        for i in range(1, numbers_length + 1):
            numbers_history[numbers[i - 1]] = i

        last_number = numbers[-1]
        with nogil:
            for turn in range(numbers_length, max_turn):
                numbers_history[last_number], last_number = turn, turn - numbers_history[last_number] if numbers_history[last_number] != 0 else 0

        return last_number
    finally:
        free(numbers_history)
