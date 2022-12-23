# Exercise 1:
def exchange_values(A:float, B:float)->float:
    '''
    Exchange 2 inputs' values without creating another variable.

    :param A: float
    :param B: float
    :return A,B: float, float; A and B after exchanging values
    '''

    A = A + B
    B = A - B
    A = A - B

    return A, B


# Exercise 2:
def is_palindrome(s:str)->bool:
    '''
    Check if the string is palindrome.

    :param s: string
    :return: boolean
    '''

    return s == s[::-1]


# Exercise 3:
def print_fizz_buzz(start:int, end:int):
    '''
    Print integers from 1 to 100(inclusive), while printing 
    Fizz/Buzz/FizzBuzz if it's multiples of 3/5/both 3 and 5.

    :param a: int
    :param b: int
    :return: none
    '''

    for num in range(start, end + 1):
        if num % 3 == 0:
            print('Fizz')
        elif num % 5 == 0:
            print('Buzz')
        elif num % 3 == 0 and num % 5 == 0:
            print('FizzBuzz')
        else:
            print(num)


# Exercise 4:
def next_biggest_prime(num:int)->int:
    '''
    Find the next biggest prime number given an arbitary integer x.

    :param n: int; Given number
    :return num: int; The next biggest prime number
    '''

    def helper_is_prime(n:int)->bool:
        for i in range(2, int(n**0.5 + 1)):
            if n % i == 0:
                return False
        return True

    if (num <= 1):
        return 2

    while True:
        num += 1
        if(helper_is_prime(num) == True):
            break

    return num


# Extra Exercise 1:
def pretty_print(n:int, char:str):
    '''
    Outputs/prints a bunch of characters according to the formats.

    :param n: int
    :param char: str
    :return: none
    '''

    if n <= 0:
        print('No output. Input n should be integer larger than 0.')

    if n == 1:
        print(char)

    for line in range(1, n+1):
        if line != 1 and line != n:
            spaces = ' ' * (n-2)
            print(char + spaces + char)
        else:
            print(n * char)


# Extra Exercise 2:
def count_perfect_square_pair(arr:list)->int:
    '''
    Given an array of numbers, create pairs (tuple) of them 
    and count the pairs of which the pair sum is a perfect square number.

    :param arr: list
    :return count: int
    '''

    count = 0

    for i in range(len(arr)):
        # if duplication is allowed, then j starts from i. If not, then j starts from i+1.
        for j in range(i+1, len(arr)):
            pair_sum = arr[i] + arr[j]

            if pair_sum <= 0 or not isinstance(pair_sum, int):
                continue
            else:
                root = pair_sum**0.5
                if int(root)**2 == pair_sum:
                    count += 1

    return count


if __name__ == "__main__":
    # Exercise 1
    print('Exercise 1')
    A, B = 14, 41
    print('Values before exchange: A = {}, B = {}'.format(A,B))
    A, B = exchange_values(A,B)
    print('Values after exchange: A = {}, B = {}'.format(A,B))

    # Exercise 2
    print('\nExercise 2')
    test_cases = ['kayak', 'level', 'good']
    for case in test_cases:
        print('{} is palindrome: {}'.format(case, is_palindrome(case)))
    
    # Exercise 3
    print('\nExercise 3')
    print_fizz_buzz(1, 100)

    # Exercise 4
    print('\nExercise 4')
    test_num = 99
    res = next_biggest_prime(test_num)
    if res is not None:
        print('The next biggest prime number of {}: {}'.format(test_num, res))

    # Extra Exercise 1
    print('\nExtra Exercise 1')
    test_num = 5
    test_char = '*'
    pretty_print(test_num, test_char)

    # Extra Exercise 2
    print('\nExtra Exercise 2')
    text_list = [1, 2, 3, 4]
    res = count_perfect_square_pair(text_list)
    print('Number of pairs satisfied: {}'.format(res))
