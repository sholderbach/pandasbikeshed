import pandas as pd
import argparse

def run(filename=None, escape=False, print_it=True):
    try:
        df = pd.read_clipboard(sep='\t')
    except:
        print('Could not read from clipboard. Make sure your clipboard contains tab separated data!')
        return 1
    df = df.replace(pd.np.nan, '')
    df_str = df.to_latex(escape=escape, index=False)
    if filename:
        with open(filename, 'w') as f:
            f.write(df_str)
    if print_it:
        print(df_str)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='clip2tex', description='A small command-line tool to convert tables copied to the clipboard e.g. from MS Excel or GDrive to a simple LaTeX')
    parser.add_argument('FILENAME', nargs='?')
    parser.add_argument('--escape', '-e', action='store_true', help='Set to escape all special characters')
    args = parser.parse_args()
    if args.FILENAME:
        run(filename=args.FILENAME, escape=args.escape, print_it=False)
    else:
        run(escape=args.escape)

