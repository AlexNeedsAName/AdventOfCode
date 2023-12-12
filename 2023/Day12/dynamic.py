#!/usr/bin/env python3
import argparse
import functools
import itertools

DEBUG=True
def dbg_print(*args, level=1, **kwargs):
    if DEBUG >= level:
        print(*args, **kwargs)


#@functools.cache
def get_groups(string):
    group_size = 0
    results = []
    for char in string:
        if char == '#':
            group_size+=1
        elif group_size > 0:
            results.append(group_size)
            group_size = 0
    if group_size > 0:
        results.append(group_size)

    return tuple(results)

def is_valid(string, groups):
    return get_groups(string) == groups


def room_for_group(string, length, end=False):
    dbg_print(f"is there room for {length} in {string}? (it is {'' if end else 'not '}the end)", level=2)
    if length < 0:
        dbg_print("no, it's negative", level=2)
        return False
    if len(string) < length+1 and not end:
        dbg_print("no, it's too short", level=2)
        return False
    elif len(string) < length:
        dbg_print("no, it's too short, even though it doesn't need a trailing '.'", level=2)
        return False
    for c in string[:length]:
        if c == '.':
            dbg_print("no, there's a '.' in it too soon", level=2)
            return False
    if not end and string[length] == '#':
        dbg_print("no, there's a '#' right after, so the group would end up being too big", level=2)
        return False
    dbg_print("Yes, there is room", level=2)
    return True


@functools.cache
def get_arrangements(string, groups, count_only):
    dbg_print(f'get_arrangements({string}, {groups})')
    results = []
    total = 0
    index = string.find('?')
    if index == -1:
        dbg_print("No choices left to make")
        if is_valid(string, groups):
            dbg_print("reached valid base case")
            if count_only:
                return 1
            return (string,)
        else:
            if count_only:
                return 0
            return tuple()

    if len(string) < sum(groups) + len(groups) - 1:
        if count_only:
            return 0
        return tuple()

    left = string[:index]
    right = string[index:]
    lgroups = get_groups(left)
    rgroups = groups[len(lgroups):]

    if lgroups == groups[:len(lgroups)]:
        dbg_print("We aren't extending an existing group")
        ret = get_arrangements(right[1:], rgroups, count_only)
        #print(f'ret = {ret}')
        if count_only:
            total += ret
        else:
            results.extend(['.'.join(a) for a in zip(itertools.repeat(left), ret)])

            # Can we add a thing without breaking our left side?            # Does the next group exist and fit here?
        if ((len(left) > 0 and left[-1] != '#') or len(left) == 0) and (len(rgroups) > 0 and room_for_group(right, rgroups[0], end=(len(right) == rgroups[0]))):
            dbg_print("Adding a new group")

            ret = get_arrangements(right[rgroups[0]+1:], rgroups[1:], count_only)
            #print(f'ret = {ret}')
            if count_only:
                total += ret
            else:
                new = '#' * rgroups[0]
                if len(right) != rgroups[0]:
                    new += '.'
                results.extend([new.join(a) for a in zip(itertools.repeat(left), ret)])

    elif lgroups[:-1] == groups[:len(lgroups)-1] and len(lgroups) <= len(groups) and left[-1] == '#':
        # All but the last group matches, maybe we can extend it
        dbg_print("Extending existing group")
        last_group = lgroups[-1]
        needed_length = groups[len(lgroups)-1] - last_group
        end = (len(right) == needed_length)
        if room_for_group(string[index:], needed_length, end):
            ret = get_arrangements(string[index+needed_length+1:], rgroups, count_only)
            #print(f'ret = {ret}')
            if count_only:
                total += ret
            else:
                new = '#' * needed_length
                if not end:
                    new += '.'
                results.extend([new.join(a) for a in zip(itertools.repeat(left), ret)])
        else:
            dbg_print("Psych! Can't extend group, there's no room")

    if count_only:
        dbg_print(f'returning {total}')
        return total
    return tuple(results)



def part1(input_file, part2):
    just_count = part2 or True
    results = []
    total = 0
    with open(input_file, 'r') as file:
        for line in file:
            if len(line.strip()) == 0:
                break
            string, groups = line.strip().split()
            groups = tuple(int(g) for g in groups.split(','))
            if part2:
                string = '?'.join((string,) * 5)
                groups *= 5
            arrangements = get_arrangements(string, groups, count_only=just_count)
            if just_count:
                total += arrangements
                continue
#            arrangements = tuple(a for a in arrangements if is_valid(a, groups))
            print(groups, len(arrangements), arrangements)
            results.extend(arrangements)

    if just_count:
        return total
    else:
        return len(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default='input.txt')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    args = parser.parse_args()
    DEBUG = args.verbose

    print(part1(args.filename, False))
    print(part1(args.filename, True))

