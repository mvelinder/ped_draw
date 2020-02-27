#! /usr/bin/python

import sys
import os
import pandas

ped_orig = pandas.read_csv(sys.argv[1],'r', delimiter='\t')
idx0 = list(ped_orig.columns.values)[0]
idx2 = list(ped_orig.columns.values)[2]
idx3 = list(ped_orig.columns.values)[3]
ped = ped_orig.sort_values(by=[idx0, idx2, idx3])

header = "digraph G {" "\n""\t" "edge [dir=none];" "\n""\t" "graph [splines=ortho];"

def getChildCount(sample_id, samples):
  childCount = 0
  for s in samples:
    if s['paternal_id'] == sample_id or s['maternal_id'] == sample_id:
      childCount += 1
  return childCount

def getGraphString(gender, affected):
  shape = "diamond"
  fillcolor = "white"
  if gender == 1: shape = "box"
  elif gender == 2: shape = "oval"
  if affected == 2: fillcolor = "gray"
  return '[shape=' + shape + ', regular=0, color="black", style="filled" fillcolor="' + fillcolor + '"];'

def getMate(sample, sampleInfo, mateInfo):
  if sample['sample_id'] in mateInfo:
    mateSampleID = mateInfo[sample['sample_id']]
    for s in sampleInfo:
      if s['sample_id'] == mateSampleID:
        return s
  return None

# make empty lists
parent_sample_ids = []

mate_info = {}
parents = []
sample_paternal_maternal = []

sample_info = []
# populate lists of individuals
for i, sample in ped.iterrows():
  kindred_id = sample[0]
  sample_id = str(sample[1])
  paternal_id = str(sample[2])
  maternal_id = str(sample[3])
  sex = sample[4]
  affected_status = sample[5]
  graphString = None

  mate_id = None
  is_parent = False
  is_child = False
  if paternal_id == '0' and maternal_id == '0':
    is_parent = True
    parent_sample_ids.append(sample_id)
  elif paternal_id != '0' and maternal_id != '0':
    is_child = True
    sample_paternal_maternal.append(sample_id + "_" + paternal_id + "_" + maternal_id)
    parents.append(paternal_id + "_" + maternal_id)
    mate_info[paternal_id] = maternal_id
    mate_info[maternal_id] = paternal_id
  sample_info.append({
    "sample_id": sample_id,
    "graph_string": "\t\"" + sample_id + "\" " + getGraphString(int(sex), int(affected_status)),
    "gender": sex,
	"paternal_id": paternal_id,
	"maternal_id": maternal_id,
    "is_child": is_child,
    "is_parent": is_parent,
    "printed": False
    })

# print header
print(header)

# print parents first
for s in sample_info:
  if not s['is_parent'] or s['printed']: continue # if not a parent or if printed then skip
  mate = getMate(s, sample_info, mate_info)
  if mate is not None:
    if s['gender'] == 1:
      print(s["graph_string"])
      print(mate["graph_string"])
    else:
      print(mate["graph_string"])
      print(s["graph_string"])
    mate['printed'] = True
  else:
    print(s["graph_string"])
  s['printed'] = True

# print children next
for s in sample_info:
  if s['is_parent'] or s['printed']: continue # if a parent or if printed skip
  print(s['graph_string'])
  s['printed'] = True

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
