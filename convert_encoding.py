import codecs
import sys

input_file = sys.argv[1]
converted_output_file = 'converted_' + input_file

lines = []
with open(input_file) as f:
    for line in f:
        line = line.strip()
        try: 
            tmp = codecs.unicode_escape_decode(line)[0]
            lines.append(tmp)
        except:
            lines.append(line)

with open(converted_output_file, "w") as w:
    #w.write('\n'.join(lines))
    for line in lines:
        try:
            w.write(line+'\n')
        except UnicodeEncodeError:
            w.write("UnicodeEncodeError \n")
        except:
            w.write("SomeError \n")
