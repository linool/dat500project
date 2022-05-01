import sys

input_file = sys.argv[1]
sorted_output_file = 'sorted_' + input_file
lines = []
with open(input_file) as f:
    for line in f:
        line = line.strip()
        if int(line.split()[-1])>1:
            lines.append(line)
def onegram_count(line):
    try:
        tmp = int(line.split()[-1])
        return tmp
    except:
        return 1

lines.sort(key=onegram_count, reverse=True)
with open(sorted_output_file, "w") as w:
    for line in lines:
        w.write(line+'\n')
        #w.write('\n'.join(lines))

