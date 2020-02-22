#! /usr/bin/python

import sys
import os
import pandas
import math

ped = pandas.read_csv(sys.argv[1],'r', delimiter='\t')

header = "digraph G {" "\n""\t" "edge [dir=none];" "\n""\t" "graph [splines=ortho];"

unaffected_male = "[shape=box, regular=0, color=\"black\", style=\"filled\" fillcolor=\"white\"];"
affected_male = "[shape=box, regular=0, color=\"black\", style=\"filled\" fillcolor=\"grey\"];" 
unaffected_female = "[shape=oval, regular=0, color=\"black\", style=\"filled\" fillcolor=\"white\"];"
affected_female = "[shape=oval, regular=0, color=\"black\", style=\"filled\" fillcolor=\"grey\"];"
affected_unknown = "[shape=diamond, regular=0, color=\"black\", style=\"filled\" fillcolor=\"grey\"];"
unaffected_unknown = "[shape=diamond, regular=0, color=\"black\", style=\"filled\" fillcolor=\"white\"];"

print(header)

# make empty lists
parent_sample_ids = []
children_sample_ids = []

unaffected_male_parent_sample_ids = []
unaffected_female_parent_sample_ids = []
unaffected_unknown_parent_sample_ids = []

affected_male_parent_sample_ids = []
affected_female_parent_sample_ids = []
affected_unknown_parent_sample_ids = []

unaffected_male_children_sample_ids = []
unaffected_female_children_sample_ids = []
unaffected_unknown_children_sample_ids = []

affected_male_children_sample_ids = []
affected_female_children_sample_ids = []
affected_unknown_children_sample_ids = []

parents = []
dads = {}
moms = {}
sample_paternal_maternal = []

# populate lists of individuals
for i, sample in ped.iterrows():
  kindred_id = sample[0]
  sample_id = str(sample[1])
  paternal_id = str(sample[2])
  maternal_id = str(sample[3])
  sex = sample[4]
  affected_status = sample[5]
  if paternal_id == '0' and maternal_id == '0':
    parent_sample_ids.append(sample_id)
    if affected_status == 1:
      if sex == 2:
        unaffected_female_parent_sample_ids.append(sample_id)
      elif sex == 1:
        unaffected_male_parent_sample_ids.append(sample_id)
      else:
        unaffected_unknown_parent_sample_ids.append(sample_id)
    elif affected_status == 2:
      if sex == 2:
        affected_female_parent_sample_ids.append(sample_id)
      elif sex == 1:
        affected_male_parent_sample_ids.append(sample_id)
      else:
        affected_unknown_parent_sample_ids.append(sample_id)
  elif paternal_id != '0' and maternal_id != '0':
    children_sample_ids.append(sample_id)
    parents.append(paternal_id + "_" + maternal_id)
    dads.update({sample_id : paternal_id})
    moms.update({sample_id : maternal_id})
    sample_paternal_maternal.append(sample_id + "_" + paternal_id + "_" + maternal_id)
    if affected_status == 1:
      if sex == 2:
        unaffected_female_children_sample_ids.append(sample_id)
      elif sex == 1:
        unaffected_male_children_sample_ids.append(sample_id)
      else:
        unaffected_unknown_children_sample_ids.append(sample_id)
    elif affected_status == 2:
      if sex == 2:
        affected_female_children_sample_ids.append(sample_id)
      elif sex == 1:
        affected_male_children_sample_ids.append(sample_id)
      else:
        affected_unknown_children_sample_ids.append(sample_id)

# print lists and drawing text
for i in unaffected_female_parent_sample_ids:
  print("\t\"" + str(i) + "\" " + unaffected_female)

for i in unaffected_male_parent_sample_ids:
  print("\t\"" + str(i) + "\" " + unaffected_male)

for i in unaffected_unknown_parent_sample_ids:
  print("\t\"" + str(i) + "\" " + unaffected_unknown)

for i in affected_female_parent_sample_ids:
  print("\t\"" + str(i) + "\" " + affected_female)

for i in affected_male_parent_sample_ids:
  print("\t\"" + str(i) + "\" " + affected_male)

for i in affected_unknown_parent_sample_ids:
  print("\t\"" + str(i) + "\" " + affected_unknown)

for i in unaffected_female_children_sample_ids:
  print("\t\"" + str(i) + "\" " + unaffected_female)

for i in unaffected_male_children_sample_ids:
  print("\t\"" + str(i) + "\" " + unaffected_male)

for i in unaffected_unknown_children_sample_ids:
  print("\t\"" + str(i) + "\" " + unaffected_unknown)

for i in affected_female_children_sample_ids:
  print("\t\"" + str(i) + "\" " + affected_female)

for i in affected_male_children_sample_ids:
  print("\t\"" + str(i) + "\" " + affected_male)

for i in affected_unknown_children_sample_ids:
  print("\t\"" + str(i) + "\" " + affected_unknown)

# print "generation" nodes
gen_count = len(parent_sample_ids) - 1

pgen_nodes = []
cgen_nodes = []
for i in parents:
  pgen_nodes.append("parentnode_" + str(i))
  cgen_nodes.append("childnode_" + str(i))

pgen_nodes_uniq = []
for i in pgen_nodes:
  if i not in pgen_nodes_uniq:
    pgen_nodes_uniq.append(i)

cgen_nodes_uniq = []
for i in cgen_nodes:
  if i not in cgen_nodes_uniq:
    cgen_nodes_uniq.append(i)

for i in pgen_nodes_uniq:
  print("\t\"" + i + "\" [shape=circle,label=\"\",height=0.01,width=0.01];")

for i in cgen_nodes_uniq:
  print("\t\"" + i + "\" [shape=circle,label=\"\",height=0.01,width=0.01];")


# connect parents
parents_uniq = []
for i in parents:
  if i not in parents_uniq:
    parents_uniq.append(i)

for i in parents_uniq:
  split_parents_uniq = [i.split("_")]
  for i in split_parents_uniq:
    print("\t{rank=same; \"" + str(i[0]) + "\" -> \"parentnode_" + str(i[0]) + "_" + str(i[1]) + "\" -> " + "\"" + str(i[1]) + "\"};")

# connect parentnode(s) to childnode(s)
for i in parents_uniq:
  print("\t\"parentnode_" + str(i) + "\" -> \"childnode_" + str(i) + "\"")

# connect children to childnodes
for i in sample_paternal_maternal:
  isplit = i.split("_")
  print("\t\"childnode_" + str(isplit[1]) + "_" + str(isplit[2]) + "\" -> \"" + str(isplit[0]) + "\"")








#for i in children_sample_ids:
#  print(i)

#for i in gen_nodes:
#  print(i)
 
#for dadkey, dadval in dads.items():
#  print(dadkey, dadval)
#  for momkey, momval in moms.items():
#    print("\t\"parentnode" + dadval + momval + "\"" + " -> \"childnode" + dadval + momval + "\"")
#  print("sample is: " + k + ", " + "dad is: " + v)
# draw and connect parent nodes
#print("\t{rank=same; " + " -> ".join(str(i) for i in parent_sample_ids) + "};")

# draw and connect parent to children
#for k, v in dads.items():
#  print(k, v)
#print("\t{rank=same; " + dads

# get number of children
#children_count = len(children_sample_ids)
#tmp_children_count = children_counti

# check if even or odd number of children
#if children_count %2 == 0:
# tmp_children_count = children_count + 1

# empty list for children nodes
#children_nodes = []

# append children nodes to list and print
#for i in range(children_count):
# children_nodes.append("children_node" + str(i))
# print("\t\"children_node" + str(i) +"\" [shape=circle,label=\"\",height=0.01,width=0.01];")

# draw and connect parent nodes
#print("\t{rank=same; \"" + parent_sample_ids[0] + "\" -> \"parent_node\" -> \"" + parent_sample_ids[1] + "\"};")

# draw children nodes
#print("\t{rank=same; " + " -> ".join(str(i) for i in children_nodes) + "};")

# connect parent node to middle node
#print("\t\"parent_node\" -> \"middle_node\"")

# connect children_nodes to children
#for i, child_sample_id in enumerate(children_sample_ids):
#        print("\t\"middle_node" + "\" -> \"" + child_sample_id + "\"")

#print("children nodes to draw: " + str(tmp_children_count))
#print("number of children is: " + str(children_count))

#print("parent sample ids: " + str(parent_sample_ids))
#print("children sample ids: " + str(children_sample_ids))

print("}")
