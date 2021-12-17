import timeit

from code_to_pdf.run import main

t = timeit.timeit('main(["../"])', setup="from code_to_pdf.run import main", number=1)

main(["../", "--max-pages-per-volume", "3"])


print(f"Time of execution: {t:.2f} s")
