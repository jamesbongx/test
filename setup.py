from cx_Freeze import setup, Executable
  
setup(name = "GeeksforGeeks" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("testfunc.py")])