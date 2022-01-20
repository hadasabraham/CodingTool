
# Profiler Usage

## 1
To run profiler, run from the **Terminal**:
```shell script
python -m cProfile -o profiler/profiler.pstats main.py
```

## 2
To analyze results, run from the **Python Console**:
```python
import pstats
import contextlib
with open('profiler.out','w') as f:
    with contextlib.redirect_stdout(f):
        p = pstats.Stats('profiler/profiler.pstats')
        p.sort_stats('cumulative').print_stats(30)
```

## Note
Some IDEs like *PyCharm* have built-in support for profiling; use it.
