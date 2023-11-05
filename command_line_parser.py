from typing import Any


class CommandLineValue(object):
    def __init__(self,value:Any) -> None:
        self.__yes_values = ['y','yes','t','true','1']
        self.__no_values = ['n','no','f','false','0']
        self.__value:str = None
        if isinstance(value,str):
            self.string_value = value
        elif isinstance(value,bool):
            self.bool_value = value
        elif isinstance(value,int):
            self.int_value = value
        elif isinstance(value,float):
            self.float_value = value
    @property
    def string_value(self) -> str:
        return self.__value
    @string_value.setter
    def string_value(self,string_value:str):
        if isinstance(string_value,str):
            self.__value=string_value
        else:
            raise ValueError()
    def __not_a_valid_bool_value() -> bool:
        raise ValueError()
    
    
    @property
    def bool_value(self) -> bool:
        True if self.string_value.lower() in [self.__yes_values] else False if self.string_value.lower() in [self.__no_values] else self.__not_a_valid_bool_value()
    @bool_value.setter
    def bool_value(self,bool_value:bool):
        if isinstance(bool_value,bool):
            self.string_value = self.__yes_values[0] if bool_value else self.__no_values[0]
        else:
            raise ValueError()
    @property
    def int_value(self) -> int:
        return int(self.string_value)
    @int_value.setter
    def int_value(self,int_value:int):
        if isinstance(int_value,int):
            self.string_value = str(int_value)
        else:
            raise ValueError()
    @property
    def float_value(self) -> float:
        return float(self.string_value)
    @float_value.setter
    def float_value(self,float_value:float):
        if isinstance(float_value,float):
            self.string_value(float_value)
        else:
            raise ValueError()

class CommandLineParser(object):
    def __init__(self) -> None:
        self.__args=dict()
        self.__executable=None
        self.__key_set=False
    def parse_args(self,args:list[str]):
        for f in args:
            self.parse_arg(f)
    def parse_arg(self,arg:str):
        if self.__executable is None:
            self.__executable = arg
        elif not self.__key_set:
            pass # Stop point WIP
    