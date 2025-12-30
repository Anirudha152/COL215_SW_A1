import math
from visualize_gates import visualize_gates
from tc_generator import generate
from time import time
import random

def process_input(fn):
    blocks = []
    with open(fn, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() == '':
                continue
            blocks.append({'name': line.split()[0], 'w': int(line.split()[1]), 'h': int(line.split()[2])})
    return blocks


def process_output(outputs, bounds, fn):
    with open(fn, 'w') as file:
        file.write(f"bounding_box {bounds[0]} {bounds[1]}\n")
        for output in outputs:
            file.write(f"{output['name']} {output['x']} {output['y']}\n")


def sorter(blocks, mode='width'):
    if mode == 'width':
        # sort blocks by width in descending order, if width is the same, sort by height in descending order
        return sorted(blocks, key=lambda block: (block['w'], block['h']), reverse=True)
    elif mode == 'height':
        # sort blocks by height in descending order, if height is the same, sort by width in descending order
        return sorted(blocks, key=lambda block: (block['h'], block['w']), reverse=True)
    elif mode == 'max_side':
        # sort blocks by max side in descending order
        return sorted(blocks, key=lambda block: (max(block['w'], block['h']), block['h'], block['w']), reverse=True)
    elif mode == 'area':
        # sort blocks by area in descending order
        return sorted(blocks, key=lambda block: (block['w'] * block['h'], block['w'], block['h']), reverse=True)


def pack(blocks, fixed_param=0, mode='vertical'):
    if mode == 'vertical':
        sorted_blocks = sorter(blocks, 'height').copy()
        bins = [{'x': 0, 'y': 0, 'w': fixed_param, 'h': float('inf')}]
        outputs = []
        for block in sorted_blocks:
            for i in reversed(range(len(bins))):
                bin_ = bins[i]
                if block['w'] <= bin_['w'] and block['h'] <= bin_['h']:
                    if block['w'] == bin_['w'] and block['h'] == bin_['h']:
                        bins.pop(i)
                    elif block['w'] == bin_['w']:
                        bins[i] = {'x': bin_['x'], 'y': bin_['y'] + block['h'], 'w': bin_['w'], 'h': bin_['h'] - block['h']}
                    elif block['h'] == bin_['h']:
                        bins[i] = {'x': bin_['x'] + block['w'], 'y': bin_['y'], 'w': bin_['w'] - block['w'], 'h': bin_['h']}
                    else:
                        bins[i] = {'x': bin_['x'], 'y': bin_['y']+block['h'], 'w': bin_['w'], 'h': bin_['h'] - block['h']}
                        bins.append({'x': bin_['x'] + block['w'], 'y': bin_['y'], 'w': bin_['w'] - block['w'], 'h': block['h']})
                    outputs.append({'name': block['name'], 'x': bin_['x'], 'y': bin_['y'], 'w': block['w'], 'h': block['h']})
                    break
        bounds = (max([output['x'] + output['w'] for output in outputs]), max([output['y'] + output['h'] for output in outputs]))
        return outputs, bounds
    elif mode == 'horizontal':
        sorted_blocks = sorter(blocks, 'width').copy()
        bins = [{'x': 0, 'y': 0, 'w': float('inf'), 'h': fixed_param}]
        outputs = []
        for block in sorted_blocks:
            for i in reversed(range(len(bins))):
                bin_ = bins[i]
                if block['w'] <= bin_['w'] and block['h'] <= bin_['h']:
                    if block['w'] == bin_['w'] and block['h'] == bin_['h']:
                        bins.pop(i)
                    elif block['w'] == bin_['w']:
                        bins[i] = {'x': bin_['x'], 'y': bin_['y'] + block['h'], 'w': bin_['w'], 'h': bin_['h'] - block['h']}
                    elif block['h'] == bin_['h']:
                        bins[i] = {'x': bin_['x'] + block['w'], 'y': bin_['y'], 'w': bin_['w'] - block['w'], 'h': bin_['h']}
                    else:
                        bins[i] = {'x': bin_['x'] + block['w'], 'y': bin_['y'], 'w': bin_['w'] - block['w'], 'h': bin_['h']}
                        bins.append({'x': bin_['x'], 'y': bin_['y'] + block['h'], 'w': block['w'], 'h': bin_['h'] - block['h']})
                    outputs.append({'name': block['name'], 'x': bin_['x'], 'y': bin_['y'], 'w': block['w'], 'h': block['h']})
                    break
        bounds = (max([output['x'] + output['w'] for output in outputs]), max([output['y'] + output['h'] for output in outputs]))
        return outputs, bounds


def run_pack(blocks):
    blocks = sorter(blocks, 'width').copy()
    total_area_of_blocks = sum([block['w'] * block['h'] for block in blocks])
    skyline_width = math.ceil(math.sqrt(total_area_of_blocks) / 0.9)
    max_eff = 0
    max_i = -1
    max_mode = ''
    for i in range(blocks[0]['w'], math.ceil(skyline_width * 1.25)):
        outputs, bounds = pack(blocks, i, 'vertical')
        eff = total_area_of_blocks / (bounds[0] * bounds[1])
        if eff > max_eff:
            max_eff = eff
            max_mode = 'vertical'
            max_i = i
        print(f'Efficiency for width {i}: {eff}')
    blocks = sorter(blocks, 'height').copy()
    for i in range(blocks[0]['h'], math.ceil(skyline_width * 1.25)):
        outputs, bounds = pack(blocks, i, 'horizontal')
        eff = total_area_of_blocks / (bounds[0] * bounds[1])
        if eff > max_eff:
            max_eff = eff
            max_mode = 'horizontal'
            max_i = i
        print(f'Efficiency for height {i}: {eff}')
    outputs, bounds = pack(blocks, max_i, max_mode)
    if max_mode == 'vertical':
        print(f'Max Efficiency: {total_area_of_blocks / (bounds[0] * bounds[1])} with bounding width {max_i}')
    else:
        print(f'Max Efficiency: {total_area_of_blocks / (bounds[0] * bounds[1])} with bounding height {max_i}')
    return outputs, bounds


def main():
    for mode in ['random', 'random_low_var', 'random_high_var', 'extreme_aspect_ratio', 'random_squares']:
        for num in [25, 50, 100, 250, 500]:
            blocks = generate(write_to_file=True, mode=mode, count=num, fp=f'testcases/input_{mode}_{num}.txt')
            total_area_of_blocks = sum([block['w'] * block['h'] for block in blocks])
            start_time = time()
            outputs, bounds = run_pack(blocks)
            output_time = time() - start_time
            process_output(outputs, bounds, f'outputs/output_{mode}_{num}.txt')
            proc_ = False
            while not proc_:
                try:
                    inp_x = int(input("x: "))
                    inp_y = int(input("y: "))
                    visualize_gates(f'outputs/output_{mode}_{num}.txt', f'testcases/input_{mode}_{num}.txt',
                                    (inp_x, inp_y))
                    proc = input('Proceed? (y/n): ')
                    if proc == 'y':
                        proc_ = True
                    elif proc == 'n':
                        proc_ = False
                except:
                    pass
            with open('efficiency.txt', 'a') as file:
                file.write(f'{mode} {num} {total_area_of_blocks / (bounds[0] * bounds[1])} {output_time}s\n')
    mode = 'sample'
    for num in range(1,6):
        blocks = process_input(f'testcases/input_{mode}_{num}.txt')
        total_area_of_blocks = sum([block['w'] * block['h'] for block in blocks])
        start_time = time()
        outputs, bounds = run_pack(blocks)
        output_time = time() - start_time
        process_output(outputs, bounds, f'outputs/output_{mode}_{num}.txt')
        proc_ = False
        while not proc_:
            try:
                inp_x = int(input("x: "))
                inp_y = int(input("y: "))
                visualize_gates(f'outputs/output_{mode}_{num}.txt', f'testcases/input_{mode}_{num}.txt',
                                (inp_x, inp_y))
                proc = input('Proceed? (y/n): ')
                if proc == 'y':
                    proc_ = True
                elif proc == 'n':
                    proc_ = False
            except:
                pass
        with open('testcases/efficiency.txt', 'a') as file:
            file.write(f'{mode} {num} {total_area_of_blocks / (bounds[0] * bounds[1])} {output_time}s\n')

if __name__ == "__main__":
    main()
