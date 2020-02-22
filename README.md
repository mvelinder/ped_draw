# ped_draw
A simple python script to draw (multi generation!) pedigrees with graphviz

![quintet.png](examples/images/quintet.png "quintet.png")

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
- to-spec [ped](https://gatkforums.broadinstitute.org/gatk/discussion/7696/pedigree-ped-files) file input
- dot/[graphviz](https://graphviz.gitlab.io/)
- [eog](https://wiki.gnome.org/Apps/EyeOfGnome)

## Examples
Are in examples/

#### 3 generation pedigree
![3gen.png](examples/images/3gen.png "3gen.png")

#### "septet" pedigree
![septet.png](examples/images/septet.png "septet.png")

## Limitations
- Does not work with multi-kindred ped files, you must subset using
- Some slightly wonky behavior with 8 or more kids
- Please add others you find to Issues
