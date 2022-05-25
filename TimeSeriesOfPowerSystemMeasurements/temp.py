from tqdm import tqdm
from time import sleep

iterations = 50

pbar = tqdm(total=iterations)
for i in range(iterations):
    sleep(0.1)
    pbar.update()
pbar.close()
