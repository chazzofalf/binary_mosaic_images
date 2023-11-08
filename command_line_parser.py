from typing import Any, Callable
from sys import argv
from io import BytesIO,TextIOWrapper
from os import linesep

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
    def __not_a_valid_bool_value(self) -> bool:
        raise ValueError()
    
    
    @property
    def bool_value(self) -> bool:
        return True if self.string_value.lower() in self.__yes_values else False if self.string_value.lower() in self.__no_values else self.__not_a_valid_bool_value()
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
    def validate(self,args:list[str]):
        return CommandLineParser.__self_validate(args=args)
    @classmethod
    def __self_validate(cls,args:list[str]):
        vo=cls()
        try:
            vo.parse_args(args)
        except:
            return False
        return True
    def __init__(self) -> None:
        self.__args:dict[str,list[CommandLineValue]]=dict()
        self.__executable=None
        self.__key_set=False
        self.__key=None
        self.__escape=False
    def parse_args(self,args:list[str]):
        for f in args:
            self.parse_arg(f)
        if self.__key_set:
            self.add_to_key(self.__key,True)
    def add_to_key(self,key:str,value:Any):
        if key not in self.__args.keys():
            self.__args[key] = []
        self.__args[key].append(CommandLineValue(value=value))
    def parse_arg(self,arg:str):
        if self.__executable is None:
            self.__executable = arg
        elif not self.__key_set:
            if arg == '--':
                raise ValueError()
            elif arg == '-':
                raise ValueError()
            elif arg.startswith('--'):
                self.__key = arg[2:]
                self.__key_set=True
            elif arg.startswith('-'):
                self.parse_args([f'--{c}' for c in arg[1:]])
            else:
                raise ValueError()
        elif not self.__escape:
            if arg == '--':
                self.__escape = True
            elif arg == '-':  
                self.add_to_key(self.__key,'-')                          
            elif arg.startswith('--'):
                self.add_to_key(self.__key,True)
                self.__key = arg[2:]
            elif arg.startswith('-'):          
                self.parse_args([f'--{c}' for c in arg[1:]])
            else:
                self.add_to_key(self.__key,arg)
                self.__key_set = False
        else:
            self.add_to_key(self.__key,arg)
            self.__key_set = False
            self.__escape = False
    def iterate(self):
        return ((key,value) for key in self.__args.keys() for value in self.__args[key]) 
class BaseCommandLineOptions(object):
    def __init__(self) -> None:
        pass
    def hydrate_arg(self,key:str,value:CommandLineValue):
        print(f'{key} = {value.string_value}')
        
class BaseHelpfulCommandLineOption(object):
    def __init__(self,help_text:str,hydrate_action:Callable[[str,CommandLineValue],None]) -> None:        
        self.__help_text = help_text
        self.__hydrate_action = hydrate_action    
    @property
    def help_text(self):
        return self.__help_text
    @property
    def hydrate_action(self):
        return self.__hydrate_action
class BaseHelpfulCommandLineOptions(BaseCommandLineOptions):
    def __init__(self) -> None:
        super().__init__()
        self.__options:dict[str,BaseHelpfulCommandLineOption] = dict()
        self.__helpv:bool=False
        self.__populate_all_options()
        
    @property
    def help(self):
        return self.__helpv
    def __populate_help_options(self):
        #print('Help options populated')
        def help_cmd(key:str,value:CommandLineValue):
            #print(f'Help cmd called with key {key} and value {value.string_value}/{value.bool_value}')
            if key in ['help','h'] and value.bool_value:
                self.__help()
            else:
                raise ValueError()        
        self.__options['help'] = BaseHelpfulCommandLineOption(help_text='--help Brings up this help menu',hydrate_action=help_cmd)
        self.__options['h'] = BaseHelpfulCommandLineOption(help_text='-h Brings up this help menu',hydrate_action=help_cmd) 
    def _populate_option(self,key:str,value:BaseHelpfulCommandLineOption):
        if key not in self.__options.keys():
            self.__options[key] = value
        else:
            raise ValueError()
    def _populate_options(self) -> None:
        pass
    def __populate_all_options(self) -> None:
        self.__populate_help_options()
        self._populate_options()
    def __help(self):
        print(linesep.join([g for f in [[f'{argv[0]}:'],[''],[f.help_text for f in self.__options.values()],['']] for g in f]))        
        self.__helpv=True
    def hydrate_arg(self, key: str, value: CommandLineValue):
        if key in self.__options.keys() and not self.__options[key] is None:
            self.__options[key].hydrate_action(key,value)
        else:            
            raise ValueError(f'Key "{key}" is invalid. Valid keys are: ' + " ".join([f for f in self.__options.keys()]))  
        #return super().hydrate_arg(key, value)
    

class BaseCommandLineHydrator(object):
    def __init__(self) -> None:
        pass
    def hydrate_and_validate(self,args:CommandLineParser,output:list[BaseCommandLineOptions],exceptions:list[Exception]):
        try:
            outv=self.hydrate(args)
            output.append(outv)
            return True
        except Exception as e:
            exceptions.append(e)
            return False
    def _createOptions(self):
        return BaseCommandLineOptions()
    def hydrate(self,args:CommandLineParser):
        bclo = self._createOptions()
        for (key,value) in args.iterate():
            self.hydrate_arg(key=key,value=value,bclo=bclo)
        return bclo
    def hydrate_arg(self,key:str,value:CommandLineValue,bclo:BaseCommandLineOptions):
        bclo.hydrate_arg(key,value) # ABSTRACT
        # Does nothing but print stuff for debugging here but it this were a actual hydrator class then it would set the proper value in the BaseCommandLineOptions subclass with any error handling/processing logic

class BaseHelpfulCommandLineHydrator(BaseCommandLineHydrator):
    def __init__(self) -> None:
        super().__init__()
    def _createOptions(self):
        return BaseHelpfulCommandLineOptions()
def validate_and_hydrate_args(bclh:BaseCommandLineHydrator):
    cp=CommandLineParser()
    if cp.validate(argv):                
        cp.parse_args(argv)        
        return bclh.hydrate(cp)
    else:
        print('Not valid args')
        
if __name__ == '__main__':
    validate_and_hydrate_args(bclh=BaseCommandLineHydrator())
    cp=CommandLineParser()