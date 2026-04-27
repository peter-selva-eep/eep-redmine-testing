def greet(name):
    return f"Hello, {name}!"

def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

def main():
    name = input("Enter your name: ")
    print(greet(name))

    numbers = [1, 2, 3, 4, 5]
    total = calculate_sum(numbers)
    print("Sum of numbers:", total)

    if total > 10:
        print("The sum is greater than 10")
    else:
        print("The sum is 10 or less")

main()
