from make_py import Target
import os

action1 = Target(["t"],["file3"])
action2 = Target(["file3"],["file2"])
action3 = Target(["file2"],["file1"])

@action1.add_action
def t_Action():
  print("t")

@action2.add_action
def file3_Action():
  print("file3")
  os.system("touch file3")

@action3.add_action
def file2_Action():
  print("file2")
  os.system("touch file2")

action1()
