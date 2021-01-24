def deprefix(prefix, enum_line):
  if enum_line[1][0 : len(prefix)] != prefix:
    raise Exception('Line {} should start with "{}"'.format(enum_line[0] + 1, prefix))
  return enum_line[1][len(prefix) :]

def decode_tps_lines(lines):
  enumerated = enumerate(lines)
  try:
    while True:
      try:
        lm_count_line = next(enumerated)
      except StopIteration:
        break
      lm_count = int(deprefix('LM=', lm_count_line))
      lm_list = (next(enumerated)[1].split(' ') for _ in range(lm_count))
      lms = [tuple([float(x.replace(',', '.')) for x in lm]) for lm in lm_list]
      image = deprefix('IMAGE=', next(enumerated))
      id_ = int(deprefix('ID=', next(enumerated)))
      yield {'landmarks': lms, 'image': image, 'id': id_}
  except StopIteration:
    raise Exception('Unexpected end of TPS file')

def read_tps(filename):
  with open(filename, 'rt') as f:
    lines = [line.strip() for line in f.readlines()]
  return decode_tps_lines(lines)
