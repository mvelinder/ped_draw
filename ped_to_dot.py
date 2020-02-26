#! /usr/bin/python

import sys
import os
import pandas

ped_orig = pandas.read_csv(sys.argv[1],'r', delimiter='\t')
ped = ped_orig.sort_values(by=[list(ped_orig.columns.values)[3]])

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

parents = []
parents_print = []
childrens_print = []
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
        parents_print.append("\t\"" + sample_id + "\" " + unaffected_female)
      elif sex == 1:
        parents_print.append("\t\"" + sample_id + "\" " + unaffected_male)
      else:
        parents_print.append("\t\"" + sample_id + "\" " + unaffected_unknown)
    elif affected_status == 2:
      if sex == 2:
        parents_print.append("\t\"" + sample_id + "\" " + affected_female)
      elif sex == 1:
		parents_print.append("\t\"" + sample_id + "\" " + affected_male)
      else:
        parents_print.append("\t\"" + sample_id + "\" " + affected_unknown)
  elif paternal_id != '0' and maternal_id != '0':
    parents.append(paternal_id + "_" + maternal_id)
    sample_paternal_maternal.append(sample_id + "_" + paternal_id + "_" + maternal_id)
    if affected_status == 1:
      if sex == 2:
        childrens_print.append("\t\"" + sample_id + "\" " + unaffected_female)
      elif sex == 1:
        childrens_print.append("\t\"" + sample_id + "\" " + unaffected_male)
      else:
	    childrens_print.append("\t\"" + sample_id + "\" " + unaffected_unknown)
    elif affected_status == 2:
      if sex == 2:
        childrens_print.append("\t\"" + sample_id + "\" " + affected_female)
      elif sex == 1:
        childrens_print.append("\t\"" + sample_id + "\" " + affected_male)
      else:
        childrens_print.append("\t\"" + sample_id + "\" " + affected_unknown)

# print parent samples
for p in parents_print:
  print(p)

# print children samples
for c in childrens_print:
  print(c)

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

print("}")
