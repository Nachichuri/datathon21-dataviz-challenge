def get_clean_serie_name(serie_title):
  '''
  Eliminates the episode and season information from an episode name, returning the serie title alone.

  Arguments:
  serie_title(str): contains an episode title with the strings 'T:<N>' or 'Ep:<NN>' in it.
  '''
  sanitized_name = []

  for word in serie_title.split():
    if word.startswith(('T:', 'Ep:')):
      continue
    else:
      sanitized_name.append(word)

  return ' '.join(sanitized_name)
