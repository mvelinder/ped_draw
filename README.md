# ped_draw
A simple python script to draw (multi generation!) pedigrees with graphviz

![septet.png](examples/images/septet.png "septet.png")

![3gen.png](examples/images/3gen.png "3gen.png")

## Usage
Make dot (to stdout):
```
python ped_to_dot.py $PED
```
or from stdin

```
grep ^kindred01 $PED | python ped_to_dot.py /dev/stdin
```

Make dot, png and view:
```
python ped_to_dot.py $PED | dot -T png -o your.png ; eog your.png
```

## Examples
Are in examples/

## Limitations
- Some slightly wonky behavior with 8 or more kids
