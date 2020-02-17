# ped_draw
Easy pedigree drawing with Graphviz

## Purpose
A simple python script to draw pedigrees with Graphviz

![tmp.png](tmp.png "tmp.png")

## Usage
Make dot (to stdout):
```
python ped_to_dot.py $PED
```

Make dot, png and view:
```
python ped_to_dot.py $PED | dot -T png -o your.png ; eog your.png
```

## Examples
Examples can be found in examples/

## Limitations
- Currently only works on 2 generation pedigrees (parents and their children)
- `ped_to_dot_3gen_dev.py` is a work in progress for 3+ generation pedigree drawing
