from  cx_Freeze import  setup ,Executable

setup(name ="simple object Detection Software",Version="0.1",
      description="this software detects objects in realtime",
      executables = [Executable("ObjectDetection_Main.py")])