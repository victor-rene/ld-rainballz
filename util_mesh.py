def create_mesh(filename, width, height):
    with open(filename, 'w') as f:
        for y in reversed(range(height+1)):
            for x in range(width+1):
                pct_x = float(x) / width
                pct_y = float(y) / height
                f.write('%.2f %.2f ' % (pct_x, pct_y))
            f.write('\n')

if __name__ == '__main__':
    create_mesh('test.mesh', 16, 9)
