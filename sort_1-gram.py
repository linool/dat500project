import codecs
lines = []
with open("1-gram_output_original.txt") as f:
    for line in f:
        line = line.strip()
        #lines.append(codecs.unicode_escape_decode(line)[0])
        lines.append(line)
def onegram_count(line):
    return int(line.split()[1])
lines.sort(key=onegram_count, reverse=True)
with open("sorted_1-gram_output_original.txt", "w") as w:
    #w.write('\n'.join(lines))
    for line in lines:
        w.write(line+'\n')
