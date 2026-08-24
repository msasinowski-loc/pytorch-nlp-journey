import pandas as pd
import numpy as np

data = {
    'language': ['fr-FR', 'fr-FR', 'fr-FR', 'de-DE', 'de-DE', 'de-DE', 'es-ES', 'es-ES', 'es-ES'],
    'source':   ['Update available', 'Click confirm', 'Contact support',
                 'Update available', 'Click confirm', 'Contact support',
                 'Update available', 'Click confirm', 'Contact support'],
    'target':   ['Mise à jour', 'Cliquez confirmer', None,
                 'Update verfügbar', None, 'Support kontaktieren',
                 'Actualización', 'Haga clic', 'Contacte soporte'],
    'src_len':  [2, 2, 2, 2, 2, 2, 2, 2, 2],
    'tgt_len':  [3, 2, None, 2, None, 2, 1, 3, 2]
}

df = pd.DataFrame(data)
print(df)

# Count total segments per language
print(df.groupby('language')['source'].count())

# Count non-null targets per language (translated segments only)
print(df.groupby('language')['target'].count())