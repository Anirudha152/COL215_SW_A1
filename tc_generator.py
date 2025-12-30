import random


def cap(h,w,height_range=(1,100),width_range=(1,100)):
    if h < height_range[0]:
        h = height_range[0]
    elif h > height_range[1]:
        h = height_range[1]
    if w < width_range[0]:
        w = width_range[0]
    elif w > width_range[1]:
        w = width_range[1]
    return h,w


def generate(write_to_file=True, fp="input.txt", mode="random", count=1000, width_range=(1, 100), height_range=(1, 100), thin_frac=0.5):
    if mode == "random":
        blocks = []
        for i in range(count):
            blocks.append({'name': f'g{i+1}', 'w': random.randint(width_range[0], width_range[1]), 'h': random.randint(height_range[0], height_range[1])})
        if write_to_file:
            with open(fp, 'w') as file:
                for block in blocks:
                    file.write(f"{block['name']} {block['w']} {block['h']}\n")
        return blocks
    elif mode == "random_low_var":
        raw_av_w = (width_range[0] + width_range[1])//2
        raw_av_h = (height_range[0] + height_range[1])//2
        w_range = width_range[1] - width_range[0]
        h_range = height_range[1] - height_range[0]
        avgw = random.randint(raw_av_w-w_range//10, raw_av_w+w_range//10)
        avgh = random.randint(raw_av_h-h_range//10, raw_av_h+h_range//10)
        blocks = [{'name': 'g1', 'w': avgw, 'h': avgh}]
        for i in range(2, count+1):

            if i % 2 == 0:
                w = random.randint(max(avgw - 20, 0), avgw)
                h = random.randint(max(avgh - 20, 0), avgh)
            else:
                w = random.randint(avgw, min(avgw + 20, 100))
                h = random.randint(avgw, min(avgh + 20, 100))
            blocks.append({'name': f'g{i}', 'w': w, 'h': h})
            avgw = (i * avgw + w) // (i + 1)
            avgh = (i * avgh + h) // (i + 1)
        if write_to_file:
            with open(fp, 'w') as file:
                for block in blocks:
                    file.write(f"{block['name']} {block['w']} {block['h']}\n")
        return blocks
    elif mode == "random_high_var":
        raw_av_w = (width_range[0] + width_range[1]) // 2
        raw_av_h = (height_range[0] + height_range[1]) // 2
        w_range = width_range[1] - width_range[0]
        h_range = height_range[1] - height_range[0]
        avgw = random.randint(raw_av_w - w_range // 10, raw_av_w + w_range // 10)
        avgh = random.randint(raw_av_h - h_range // 10, raw_av_h + h_range // 10)
        blocks = [{'name': 'g1', 'w': avgw, 'h': avgh}]
        for i in range(2, count + 1):
            if i % 5 == 0:
                w = random.randint(45, 55)
                h = random.randint(45, 55)
            elif i % 2 == 0:
                w = random.randint(0, 20)
                h = random.randint(0, 20)
            else:
                w = random.randint(80, 100)
                h = random.randint(80, 100)
            blocks.append({'name': f'g{i}', 'w': w, 'h': h})
            avgw = (i * avgw + w) // (i + 1)
            avgh = (i * avgh + h) // (i + 1)
        if write_to_file:
            with open(fp, 'w') as file:
                for block in blocks:
                    file.write(f"{block['name']} {block['w']} {block['h']}\n")
        return blocks
    elif mode == "extreme_aspect_ratio":
        num_thin = int(count * thin_frac)
        num_wide = count - num_thin
        blocks = []
        for i in range(num_thin):
            blocks.append({'name': f'g{i+1}', 'w': random.randint(width_range[0]//2 + width_range[1]//2, width_range[1]), 'h': random.randint(height_range[0], height_range[0] + width_range[1]//10 + width_range[0]//10)})
        for i in range(num_wide):
            blocks.append({'name': f'g{num_thin+i+1}', 'w': random.randint(width_range[0], width_range[0] + height_range[1]//10 + height_range[0]//10), 'h': random.randint(height_range[0]//2 + height_range[1]//2, height_range[1])})
        if write_to_file:
            with open(fp, 'w') as file:
                for block in blocks:
                    file.write(f"{block['name']} {block['w']} {block['h']}\n")
        return blocks
    elif mode == "random_squares":
        blocks = []
        for i in range(count):
            side = random.randint(max(width_range[0], height_range[0]), min(width_range[1], height_range[1]))
            blocks.append({'name': f'g{i+1}', 'w': side, 'h': side})
        if write_to_file:
            with open(fp, 'w') as file:
                for block in blocks:
                    file.write(f"{block['name']} {block['w']} {block['h']}\n")
        return blocks
