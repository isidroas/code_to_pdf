import timeit

from code_to_pdf.run import main

main(["../", "--max-pages-per-volume", "3"])

t = timeit.timeit('main(["../"])', setup="from code_to_pdf.run import main", number=1)

print(f"Time of execution: {t:.2f} s")
