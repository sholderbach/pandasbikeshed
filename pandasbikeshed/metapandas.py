import os
import re
import pandas as pd

# TODO: find a solution to implement nice metadata formats


def read_with_metadata_dict(filename):
    """
    Returns: data, metadata
    """
    metadata = {}
    with open(filename) as fh:
        # Process a contiguous block of metadata
        # format '# var_name: value'
        for line in fh:
            if line.startswith('#'):
                lsplits = line.strip().split(' ')
                try:
                    meta = int(lsplits[2])
                except ValueError:
                    meta = lsplits[2]
                metadata[lsplits[1][:-1]] = meta
            else:
                break
    data = pd.read_csv(filename, sep='\t', comment='#', )
    return data, metadata


def write_with_metadata_dict(filename, data, metadata):
    metadata_str = metadata_to_str(metadata)
    with open(filename, 'wt') as fh:
        fh.write(metadata_str)
        data.to_csv(fh, sep='\t', index=False)


def metadata_to_str(metadata):
    metadata_str = '\n'.join(
        ['# {name}: {dat}'.format(name, dat)
         for name, dat in metadata.items()]
    ) + '\n'
    return metadata_str
