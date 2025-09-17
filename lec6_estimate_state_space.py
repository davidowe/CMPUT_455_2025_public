
def estimate_by_level_branching(branching_factors):
    space_total = 1
    for i in range(len(branching_factors)):
        level_total = 1
        for n in range(i+1):
            level_total *= branching_factors[n]
        space_total += level_total
    return space_total

for size in range(1, 7):
    print("State space estimate for ", size, "x", size, " board:", sep="")
    starting_moves = size * size
    state_space_size = estimate_by_level_branching([starting_moves-i for i in range(starting_moves)])
    print(f"{state_space_size:.2e}")
    print("Estimated time to explore all states at a rate of 466k nodes/second")
    est_time = state_space_size/466000
    if est_time < 60:
        print(est_time, "seconds")
    else:
        est_time /= 60
        if est_time < 60:
            print(est_time, "minutes")
        else:
            est_time /= 60
            if est_time < 24:
                print(est_time, "hours")
            else:
                est_time /= 24
                if est_time < 365:
                    print(est_time, "days")
                else:
                    est_time /= 365
                    if est_time < 100:
                        print(est_time, "years")
                    else:
                        est_time /= 100
                        print(est_time, "centuries")
