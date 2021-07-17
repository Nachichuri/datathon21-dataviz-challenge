def get_clean_serie_name(serie_title):
  sanitized_name = []

  for word in serie_title.split():
    if word.startswith(('T:', 'Ep:')):
      continue
    else:
      sanitized_name.append(word)

  return ' '.join(sanitized_name)