#!/usr/bin/env python3
import sys
import os
import re
import json
import html

#its easier to think about trees if we model them as such
class Tree(object):
  def __init__(self, name = None, parent = None):
    if parent is not None:
      if not isinstance(parent, Tree):
        raise Exception('Parent must be a tree type')
      else:
        self.depth = parent.depth + 1
    else:
      self.depth = 0
    self.name = name
    self.parent = parent
    self.children = []

  def root(self):
    root = self
    while root.parent is not None:
      root = root.parent
    return root

  def push(self, name):
    self.children.append(Tree(name, self))

  def to_dict(self):
    if self.name:
      return { self.name : [ c.to_dict() for c in self.children ] } if re.match('^G[0-9]+ ', self.name) else self.name
    else:
      return [ c.to_dict() for c in self.children ]

  def print_txt(self):
    if self.parent:
      sys.stdout.write(''.join([' ' * (self.depth - 1) * 2, self.name, os.linesep]))
    for c in self.children:
      c.print_txt()
  def print_html(self):
    indent = ' ' * (self.depth - 1) * 2
    #render the info i have
    if self.parent:
      if self.parent.parent and self is self.parent.children[-1]:
        sys.stdout.write(''.join([indent, '<li class="lastChild">', html.escape(self.name), os.linesep]))
      else:
        sys.stdout.write(''.join([indent, '<li>',  html.escape(self.name), os.linesep]))
      if self.children:
        sys.stdout.write(''.join([indent, '<ul class="collapsibleList">', os.linesep]))
    else:
      sys.stdout.write(''.join([indent, '<ul class="treeView">', os.linesep]))

    #render the children
    for child in self.children:
      child.print_html()

    #close out my info
    if self.parent:
      if self.children:
        sys.stdout.write(''.join([indent, '</ul>', os.linesep]))
      sys.stdout.write(''.join([indent, '</li>', os.linesep]))
    else:
      sys.stdout.write(''.join([indent, '</ul>', os.linesep]))
  def print_json(self):
    sys.stdout.write(json.dumps(self.to_dict()))


if __name__ == "__main__":

  tree = Tree()
  line_no = 0

  #build the tree
  try:
    #run through the input
    for line in sys.stdin:
      line_no += 1
      #parse the indent
      i = (len(line) - len(line.lstrip())) / 2
      #if we are diving deeper
      if tree.depth < i:
        #you cant go more than one at a time downwards
        if i - tree.depth > 1:
          raise Exception('Cannot deepen the indent by more than one at a time')
        tree = tree.children[-1]
      #if we are popping back up
      elif tree.depth > i:
        while i < tree.depth:
          tree = tree.parent
      #add this info to this trees children
      tree.push(line.strip())
  except Exception as e:
    sys.stderr.write('%s at line: %d' % (repr(e), line_no))
    sys.exit(1)

  #print the tree again
  #tree = tree.root()
  #tree.print_txt()

  #print some html lists
  tree = tree.root()
  tree.print_html()

  #print as json
  #tree = tree.root()
  #tree.print_json()