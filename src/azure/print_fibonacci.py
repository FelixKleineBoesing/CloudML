
def print_fibonacci():
    values = [0, 1]
    for i in range(10):
        values.append(values[-1] + values[-2])
    print(", ".join([str(val) for val in values]))


if __name__ == "__main__":
    print_fibonacci()