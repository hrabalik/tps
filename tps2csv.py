import sys
import read_tps

def out(x):
  print(x, end='')

if __name__ == '__main__':
  entries = [entry for entry in read_tps.read_tps(sys.argv[1])]
  max_lm_count = max((len(entry['landmarks']) for entry in entries))
  out('id,image')
  for i in range(max_lm_count):
    out(',x{},y{}'.format(i, i))
  out('\n')
  for entry in entries:
    out(str(entry['id']) + ',' + entry['image'])
    for lm in entry['landmarks']:
        out(',' + str(lm[0]) + ',' + str(lm[1]))
    out(',' * (2 * (max_lm_count - len(entry['landmarks']))))
    out('\n')
