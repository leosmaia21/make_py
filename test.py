from make_py import Target
import os

action1 = Target("t",["t"],["file3"])
action3 = Target("file2", ["file2"],["file1"])
action2 = Target("file3", "file3",action3)


@action1
def t_Action():
  os.system("touch t")

@action2
def file3_Action():
  print("file3")
  os.system("touch file3")

@action3
def file2_Action():
  print("file2")
  os.system("touch file2")


try:

  action1()
except Exception as e:
  print(e)
