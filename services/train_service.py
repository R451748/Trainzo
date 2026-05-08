from datetime import datetime
import random

def get_train_data(train_no):

    return {

        'trainNo': train_no,

        'latitude':
            12.9716 + random.uniform(-1, 1),

        'longitude':
            77.5946 + random.uniform(-1, 1),

        'speed':
            random.randint(40, 120),

        'lastUpdated':
            datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S'
            )
    }