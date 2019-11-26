from faker import Factory
import random

faker = Factory.create()
# probability of typo
prob = 0.3

def delete_char(name):
    """
    Remove a character at random from the string    
    Parameters
    ---
        str name: string to remove a character from
    
    Returns:
        str name: perturbed string

    """
    # remove random character from string
    ind = random.randint(1,len(name)-1)
    name = name[:ind-1] + name[ind:]
    return name

def swap_chars(name):
    """
    Swap two characters in a string at random.
    """
    name_len = len(name)
    ind = random.randint(0,name_len-2)
    if name[ind].isspace(): # don't swap with spaces
        return swap_chars(name)
    name = name[:ind] + name[ind+1] + name[ind] + name[ind+2:]
    return name

def shuffle_letters(name):
    """
    Performs one, two,  or three character swaps.
    """
    num_times = random.randint(1,3)
    for _ in range(num_times):
        name = swap_chars(name)
    return name

def chop_letter(name):
    """
    Removes the last character of the name half the time.
    The other half, remove the first character.
    """
    if random.random() < 0.5:
        return name[:-1]
    else:
        return name[1:]

def perturb(name, r=None):
    """
    Choose one of several ways to perturb a string, 
    and perform the change to the given `name`.
    """
    if r is None:
        r = random.randint(0,3)
    elif type(r) is float or type(r) is int:
        if r<0 or r>=4:
            raise ValueError("Please specify 0 <= r < 4")
    else:
        raise TypeError("r must be a number")
    
    if r == 0:
        return delete_char(name)
    elif r == 1:
        return swap_chars(name)
    elif r == 2:
        return shuffle_letters(name)
    elif r == 3:
        return chop_letter(name)

def main():
    import argparse
    desc = "Typo Corrector!"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-n', '--number',
                        default=100,
                        type=int,
                        help='Number of unique names.')  
    parser.add_argument('-r', '--repeats',
                        default=25,
                        type=int,
                        help='Max number of times a single name occurs.')  
    args = parser.parse_args()
    num_names = args.number
    max_num_repeats = args.repeats
    # TODO add argparse
    # create original list (typo free)
    num_changes = 0
    num_lines = 0
    print("Making typo list from %d unique names with up to %d repetitions."%(num_names, max_num_repeats))
    with open('wordlist.txt', 'w') as f:
        for i in range(num_names):
            # pick out random lines to perturb (make typo)
            name = faker.company()
            num_repeats = random.randint(1,max_num_repeats) 
            num_lines += num_repeats
            for _ in range(num_repeats):
                if random.random() < prob:
                    new_name = perturb(name)
                    num_changes +=1
                else:
                    new_name = name
                f.write(new_name + '\n')
    print("Num changes: %d\nNum lines: %d"%(num_changes, num_lines))

if __name__ == '__main__':
    main()
