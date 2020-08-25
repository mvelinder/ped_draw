#! /usr/bin/python

import sys
import os

def getInvisibleNodes(prefix, labels):
  return '{%s [shape=point width=0 style=invis]};' % ",".join([prefix + "_" + sID for sID in labels])

def getSpouseRank(a, spouseConnection, b):
  return '{rank=same; %s -- spouse_%s -- %s};' % (a, spouseConnection, b)

def getConnection(a, b):
  return "%s -- %s;" % (a, b)

def getChildConnection(a, b):
  return "children_%s -- %s;" % (a, b)

def getSpouseChildConnectionNode(sr):
  return "spouse_%s -- children_%s" % (sr, sr)

def getSpouseWithAllNodes(sample):
  sortedSpouseRelationship = [sample, sample.spouse]
  connectionNode = "%s_%s" % (sortedSpouseRelationship[0].sample_id, sortedSpouseRelationship[1].sample_id)
  lines = []
  lines.append(sortedSpouseRelationship[0].getGraphNodeString())
  lines.append(sortedSpouseRelationship[1].getGraphNodeString())
  lines.append("{spouse_%s [shape=point width=0 style=invis]};"%connectionNode)
  lines.append("{rank=same; %s -- spouse_%s -- %s};" %(sortedSpouseRelationship[0].sample_id, connectionNode, sortedSpouseRelationship[1].sample_id))
  if len(sample.children) > 0:
    lines.append("{children_%s [shape=point width=0 style=invis]};"%connectionNode)
    lines.append("spouse_%s -- children_%s" % (connectionNode, connectionNode))
  return {'lines': lines, 'connectionNode': connectionNode}

def sortSamplesBySpouse(samples):
  sortedSampleIDs = []
  for sampleID in samples:
    if sampleID in sortedSampleIDs: continue
    sample = samples[sampleID]
    if len(sample.parents) == 0:
      if sample.spouse is not None:
        sortedSampleIDs = sortedSampleIDs + sample.getSortedSpouseRelationship()
      else:
        sortedSampleIDs.append(sampleID)

  for sampleID in samples:
    if sampleID in sortedSampleIDs: continue
    sample = samples[sampleID]
    if sample.spouse is not None:
      sortedSampleIDs = sortedSampleIDs + sample.getSortedSpouseRelationship()
    else:
      sortedSampleIDs.append(sampleID)

  return sortedSampleIDs



class Sample:
  def __init__(self, kindred_id, sample_id, paternal_id, maternal_id, sex, affected_status):
    self.kindred_id = kindred_id
    self.sample_id = str(sample_id)
    self.paternal_id = str(paternal_id)
    self.maternal_id = str(maternal_id)
    self.sex = sex
    self.affected_status = affected_status
    self.spouse = None
    self.parents = {}
    self.siblings = {}
    self.children = {}
    self.parent_order = []

  def setSpouse(self, spouse):
    self.spouse = spouse

  def addParent(self, parentSample):
    self.parents[parentSample.sample_id] = parentSample

  def addChild(self, childSample):
    self.children[childSample.sample_id] = childSample

  def addSibling(self, siblingSample):
    self.siblings[siblingSample.sample_id] = siblingSample

  def getSortedSpouseRelationshipSamples(self):
      if self.spouse is None:
        return []
      if self.sex == 1:
        return [self, self.spouse]
      else:
        return [self.spouse, self]

  def getSortedSpouseRelationship(self):
      if self.spouse is None:
        return []
      if self.sex == 1:
        return [self.sample_id, self.spouse.sample_id]
      else:
        return [self.spouse.sample_id, self.sample_id]

  def getSortedSpouseRelationshipString(self):
    if self.spouse is None:
      return ''
    return '_'.join(self.getSortedSpouseRelationship())

  def getGraphNodeString(self):
    fillcolor = "white"
    if self.affected_status == 2:
      fillcolor = "gray"
    shape = "diamond"
    if self.sex == 1: shape = "box"
    elif self.sex == 2: shape = "oval"
    return '"'+self.sample_id+'" [shape=' + shape + ', regular=0, color="black", style="filled" fillcolor="' + fillcolor + '"];'


samples = {}
# ped = pandas.read_csv(sys.argv[1],'r', delimiter='\t')
# for i, sample in ped.iterrows():
pedFile = open(sys.argv[1],'r')
headerProcessed = False
for sampleLine in pedFile:
  if not headerProcessed:
    headerProcessed = True
    continue

  sample = sampleLine.replace('\n', '').split('\t')
  # sample = sampleSplit # {cols[i] : sampleSplit[i] for i in range(len(cols))}

  kindred_id = sample[0]
  sample_id = str(sample[1])
  paternal_id = str(sample[2])
  maternal_id = str(sample[3])
  sex = int(sample[4])
  affected_status = int(sample[5])
  graphString = None
  sample = Sample(kindred_id, sample_id, paternal_id, maternal_id, sex, affected_status)
  samples[sample_id] = sample

sortedSamples = sorted(samples.values(), key=lambda s: s.sample_id)
for sample in sortedSamples:
  sampleID = sample.sample_id
  if sample.paternal_id != '0' and sample.maternal_id != '0':
    pat = samples[sample.paternal_id]
    mat = samples[sample.maternal_id]
    pat.setSpouse(mat)
    mat.setSpouse(pat)
  for tmpSample in sortedSamples:
    tmpSampleID = tmpSample.sample_id
    if tmpSampleID == sampleID: continue # don't compare to yourself
    # add parent child relationships
    if tmpSample.paternal_id == sampleID or tmpSample.maternal_id == sampleID:
      sample.addChild(tmpSample)
      tmpSample.addParent(sample)
    # add sibling relationships
    if tmpSample.paternal_id == sample.paternal_id or tmpSample.maternal_id == sample.maternal_id:
      sample.addSibling(tmpSample)
      tmpSample.addSibling(sample)

#https://stackoverflow.com/questions/27504703/in-graphviz-how-do-i-align-an-edge-to-the-top-center-of-a-node/36953206
#model after test.dot
nodes = {'male': [], 'female': [], 'spouse': [], 'children': [], 'children_samples': []}
for sampleID in sortSamplesBySpouse(samples):
  sample = samples[sampleID]
  sortedSpouseRelationship = sample.getSortedSpouseRelationshipString()
  if len(sortedSpouseRelationship) > 0 and sortedSpouseRelationship not in nodes['spouse']:
    nodes['spouse'].append(sortedSpouseRelationship)
    if len(sample.children) > 0:
      for c in sample.children: nodes['children_samples'].append(samples[c])
      if sortedSpouseRelationship not in nodes['children']:
        nodes['children'].append(sortedSpouseRelationship)

printed = set()
print("graph G {")
print("\tedge [dir=none];")
print("\tgraph [splines=ortho concentrate=true];")
spousesThatNeedParentConnections = []
nodes = [s for s in list(samples.values()) if len(s.parents) == 0]
while len(nodes) > 0:
  sample = nodes[0]
  nodes.pop(0)
  if sample.sample_id in printed: continue
  sample = samples[sample.sample_id]
  spouseInfo = ''
  if sample.spouse is None and sample.sample_id not in printed:
    print("\t" + sample.getGraphNodeString())
    printed.add(sample.sample_id)
  elif sample.spouse is not None:
    printed.add(sample.spouse.sample_id)
    for sp in list(sample.spouse.parents.values()): nodes.insert(0, sp)
    if len(sample.spouse.parents) > 0:
      spousesThatNeedParentConnections.append(sample.spouse)
    spouseInfo = getSpouseWithAllNodes(sample)
    for line in spouseInfo['lines']:
      if line not in printed:
        print("\t" + line)
        printed.add(line)
  if len(sample.parents) > 0:
    parentNodeConnectorLabel = "%s_%s" % (sample.parent_order[0].sample_id, sample.parent_order[1].sample_id)
    childNodeConnector = "children_%s -- %s" % (parentNodeConnectorLabel, sample.sample_id)
    if childNodeConnector not in printed:
      print("\t"+childNodeConnector)
      printed.add(childNodeConnector)
  for childID in sample.children:
    child = samples[childID]
    child.parent_order = [sample, sample.spouse]
    if any(s.sample_id == child.sample_id for s in nodes) or len(spouseInfo) == 0: continue
    nodes.insert(0, child)
for spouse in spousesThatNeedParentConnections:
  parentNodeConnectorLabel = "%s_%s" % (spouse.parent_order[0].sample_id, spouse.parent_order[1].sample_id)
  childNodeConnector = "children_%s -- %s" % (parentNodeConnectorLabel, spouse.sample_id)
  if childNodeConnector not in printed:
    print("\t"+childNodeConnector)
    printed.add(childNodeConnector)
print("}")
