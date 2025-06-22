import os


def check_all_str(values):
  if isinstance(values, str):
    return True
  return all([isinstance(item, str) for item in values])

def check_timestamp(targets, deps):
  target_times = {file: os.path.getmtime(file) for file in targets if os.path.exists(file)}
  dep_times = {file: os.path.getmtime(file) for file in deps if os.path.exists(file)}

  ret = []
  for dep_file, dep_time in dep_times.items():
    for target, target_time in target_times.items():
      if dep_time > target_time:
        ret += dep_time
  return ret


fileExist = os.path.exists

def get_timestamp(file): 
  if fileExist(file):
    return os.path.getmtime(file)
  return 0


def is_dep_newer(dep, targets):
  print(targets)
  dep_time = get_timestamp(dep)
  for target in targets:
    if get_timestamp(target) < dep_time:
      return True
  return False
      

def get_target_instance(target):
  all_targets_insts = Target.get_all_instances()
  for inst in all_targets_insts:
    if target in inst.targets:
      return inst
  return None


class Target:
  _instances = []

  def __init__(self, targets, deps, phony = False, helper = ""):
    self.targets = []
    self.deps = []
    self.actions = []

    if not check_all_str(targets):
      raise TypeError("Target is not neither a str nor a list")
    self.targets += targets


    if not check_all_str(deps):
      raise TypeError("Dep is not neither a str nor a list")
    self.deps += deps

    self.phone = phony
    if helper is not None: print(helper)
    
    Target._instances.append(self)

  @classmethod
  def get_all_instances(cls):
    return cls._instances

  def add_target(targets):
    if not check_all_str(targets):
      raise TypeError("Target is not neither a str nor a list")
    self.targets += targets

  def remove_target(targets):
    if not check_all_str(targets):
      raise TypeError("Target is not neither a str nor a list")
    if isinstance(targets, str):
      targets = [targets]

    for target in targets:
      self.targets.remove(target)

  def __call__(self):
    all_targets_insts = Target.get_all_instances()
    execute_action = False
    for dep in self.deps:
      #check if there is a target for this dep, if so execute that target
      target_to_execute = get_target_instance(dep)
      if target_to_execute is not None:
        target_to_execute()
      elif not fileExist(dep): #There is no target and the file doesn't exist
          raise Exception(f"The {dep} file doesn't exit and there is no target for it")
      elif is_dep_newer(dep, self.targets):
        execute_action = True
    
    if execute_action:
      print("ola")
      # for action in self.actions:
      #   action()

          

t = Target("t",["file3"])
file3 = Target("file3",["file2"])
file2 = Target("file2",["file1"])
file1 = Target("file1",[])

t()
