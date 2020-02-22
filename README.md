# ped_draw
A simple python script to draw (multi generation!) pedigrees with graphviz

#### 3 generation pedigree
![quintet.png](examples/images/quintet.png "quintet.png")

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

#### 3 generation pedigree
![3gen.png](examples/images/3gen.png "3gen.png")

#### "septet" pedigree
![septet.png](examples/images/septet.png "septet.png")

## Limitations
- Some slightly wonky behavior with 8 or more kids
- Please add others you find to Issues
