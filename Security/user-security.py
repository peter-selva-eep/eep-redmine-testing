def write_file(filename):
    with open(filename, 'w') as file:
        file.write("Apple\nBanana\nCherry\nMango\n")

def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def process_data(lines):
    fruits = []
    for line in lines:
        fruits.append(line.strip())
    return fruits

def main():
    filename = "fruits.txt"
    write_file(filename)

    data = read_file(filename)
    fruits = process_data(data)

    for fruit in fruits:
        print("Fruit:", fruit)

main()
