#  vim: set foldmethod=indent foldcolumn=4 :
#!/usr/bin/env python3


import pandas as pd
from collections import Counter

def get_oversampling(X, y, oversampler, kwargs=dict(sampling_strategy='auto', random_state=42)):
    # Check the class distribution before applying  the OverSampler
    print("Class distribution before OverSampler:", Counter(y))

    # Initialize the OverSampler
    _os = oversampler(**kwargs)

    # Apply OverSampler to balance the dataset
    X_resampled, y_resampled = _os.fit_resample(X, y)

    # Check the class distribution after applying OverSampler
    print("Class distribution after  OverSampler:", Counter(y_resampled))

    return X_resampled, y_resampled
