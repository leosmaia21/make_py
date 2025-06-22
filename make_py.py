import os
from types import SimpleNamespace

fileExist = os.path.exists

def check_all_str(values):
  if isinstance(values, (str, Target)):
    return True
  for value in values:
    if not isinstance(value, (str, Target)):
      return False
  return True

def get_timestamp(file): 
  if fileExist(file):
    return os.path.getmtime(file)
  return 0

def is_dep_newer(dep, targets):
  # print(targets)
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

  def __init__(self, name, targets, deps, phony = False, helper = None):
    self.targets = []
    self.deps = []
    self.actions = []
    self.name = name

    if not check_all_str(targets):
      raise TypeError("Target is neither a str nor a list")
    if isinstance(targets, (str, Target)):
      self.targets.append(targets)
    else:
      self.targets += targets


    if not check_all_str(deps):
      raise TypeError("Dep is neither a str nor a list")
    if isinstance(deps, (str, Target)):
      self.deps.append(deps)
    else:
      self.deps += deps

    self.phone = phony
    if helper: print(helper)
    
    Target._instances.append(self)

  
  def add_action(self, func):
    self.actions.append(func)
    def wrapper(*args, **kwargs):
      return func(*args, **kwargs)
    return wrapper

  def add_target(targets):
    if not check_all_str(targets):
      raise TypeError("Target is neither a str nor a list")
    self.targets += targets

  def remove_target(targets):
    if not check_all_str(targets):
      raise TypeError("Target is neither a str nor a list")
    if isinstance(targets, str):
      targets = [targets]

    for target in targets:
      self.targets.remove(target)

  @classmethod
  def get_all_instances(cls):
    return cls._instances

  def __call__(self, func = None):
    if callable(func):
      self.actions.append(SimpleNamespace(func=func, name=func.__name__))
      def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
      return wrapper

    all_targets_insts = Target.get_all_instances()
    execute_actions = len(self.deps) == 0
    deps = [item for d in self.deps for item in (d.targets if isinstance(d, Target) else [d])] #I know not the best readability but saves 5 lines!

    for dep in deps:
      #check if there is a target for this dep, if so execute that target
      target_to_execute = get_target_instance(dep)
      if target_to_execute is not None:
        target_to_execute()

      if not fileExist(dep): #There is no target and the file doesn't exist
        raise FileNotFoundError(f"The {dep} file doesn't exit and there is no target for it")
      elif is_dep_newer(dep, self.targets):
        execute_actions = True
    
    if execute_actions:
      if len(self.actions):
        print(f"Executing target: {self.name}")
      for action in self.actions:
        print(f"Executing target's action: {action.name}")
        action.func()


          

