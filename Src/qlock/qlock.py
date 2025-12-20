import argparse
from modes import fidelity, watermark

parser = argparse.ArgumentParser(description="Q-LOCK Attractor Engine")
parser.add_argument('--mode', choices=['fidelity', 'watermark'], required=True)
args = parser.parse_args()

if args.mode == 'fidelity':
    fidelity.main()
elif args.mode == 'watermark':
    watermark.main()
