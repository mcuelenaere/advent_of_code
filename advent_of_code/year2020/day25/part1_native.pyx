from libc.stdint cimport uint64_t

def determine_loop_size(uint64_t expected_outcome):
    cdef uint64_t value = 1
    cdef uint64_t loop_size = 0
    with nogil:
        while True:
            value *= 7
            value %= 20201227
            loop_size += 1
            if value == expected_outcome:
                break
    return loop_size

def transform(uint64_t subject_number, uint64_t loop_size):
    cdef uint64_t value = 1
    with nogil:
        for _ in range(loop_size):
            value *= subject_number
            value %= 20201227
    return value
