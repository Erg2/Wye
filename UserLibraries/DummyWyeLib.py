from Wye import Wye
from WyeCore import WyeCore
class DummyWyeLib:
  def _build():
    WyeCore.Utils.buildLib(DummyWyeLib)
  canSave = True  # all verbs can be saved with the library
  class DummyWyeLib_rt:
   pass #1
