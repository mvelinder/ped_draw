# ped_draw
A simple python script to draw (complex, multi generation!) pedigrees with graphviz

![3gen.png](examples/images/3gen.png "3gen.png")

## Install
```
git clone https://github.com/mvelinder/ped_draw.git
```

## Usage
Make dot (to stdout), can also read from /dev/stdin:
```
python ped_to_dot.py $PED
```

Make dot, save png and view with eog:
```
python ped_to_dot.py $PED | dot -T png -o your.png ; eog your.png
```

## Requirements
- [python](https://www.python.org/) 2.7.15 or greater
- to-spec, tab separated [ped](https://gatkforums.broadinstitute.org/gatk/discussion/7696/pedigree-ped-files) file input, including header line
- dot/[graphviz](https://graphviz.gitlab.io/)
- [eog](https://wiki.gnome.org/Apps/EyeOfGnome) or otherwise for viewing

## Examples
Are in [examples/](examples/)

#### "septet" pedigree
![septet.png](examples/images/septet.png "septet.png")

#### 4 generation pedigree
![4gen.png](examples/images/4gen.png "4gen.png")

## Issues
- If you're getting convoluted lines between parents, try sorting and piping into ped_draw with `sort -k1 -k3 -k4 -g $PED | python ped_to_dot.py /dev/stdin`
  - [examples/images/unsorted.png](examples/images/unsorted.png) [.ped](examples/unsorted.ped) before sorting, [examples/images/sorted.png](examples/images/sorted.png) [.ped](examples/sorted.ped) after sorting
- Some slightly wonky lines happen with 8 or more children per set of parents (see above)
- Does not currently support drawing between single parent-child combinations
