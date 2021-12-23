from time import time

from code_to_pdf.run import main

t1 = time()
main(["../", "--output-folder", "./", "--config-file", "./params.yaml"])
t2 = time()
main(["../"])
t3 = time()
main(["../", "--max-pages-per-volume", "3", "--title", "testing_volumes"])
t4 = time()


for diff in (t2 - t1, t3 - t2, t4 - t3):
    print(f"Time of execution: {diff:.2f} s")
