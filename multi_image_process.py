from typing import Iterable
import image_process
import os
import pathlib
import sys
import subprocess
import time
import command_line_parser
import traceback
import shutil
from command_line_parser import CommandLineValue

bconvert=CommandLineValue.bool_as_string
class MultiImageCommandLineOptionsHydrator(command_line_parser.BaseHelpfulCommandLineHydrator):
    def __init__(self) -> None:
        super().__init__()
        
    def _createOptions(self):
        return MultiImageCommandLineOptions()
    
class MultiImageCommandLineOptions(command_line_parser.BaseHelpfulCommandLineOptions):
    def __init__(self) -> None:
        super().__init__()
        self.__input_directory:str=None
        self.__output_dir:str=None
        self.__colorhex:str=None
        self.__invert:bool=None
        self.__cell_invert:bool=None
        self.__multiprocessing:bool=None
        self.__reset_output_dir:bool=None
        self.__output_width:int=None
        self.__output_height:int=None
        self.__output_size:str=None
        self.__rainbow:bool=None
        self.__palettized:bool=None
        
    def __fill_autos(self):
        self.__invert = False if self.__invert is None else self.__invert
        self.__cell_invert = False if self.__cell_invert is None else self.__cell_invert
        self.__multiprocessing = False if self.__multiprocessing is None else self.__multiprocessing
        self.__reset_output_dir = False if self.__reset_output_dir is None else self.__reset_output_dir   
        self.__rainbow = False if self.__rainbow is None else self.__rainbow
        self.__palettized = False if self.__palettized is None else self.__palettized
    def __is_one_or_none_of(self,items:Iterable[bool]):
        found_true=False
        for f in items:
            if f:
                if not found_true:
                    found_true=True
                else:
                    return False
        return True         
    def __sub_validate(self) -> bool:
        self.__fill_autos()
        return self.__input_directory is not None \
            and self.__output_dir is not None  \
                and (( self.__output_size is None and self.__output_height is None and self.__output_width is None) or \
                    (self.__output_size is None and self.__output_height is not None and self.__output_width is not None) or \
                    (self.__output_size is not None and self.__output_height is None and self.__output_width is None)
                     ) and \
                         (
                             self.__is_one_or_none_of((self.__colorhex is not None,self.__rainbow,self.__palettized))                             
                         )
    
    def validate(self) -> bool:
        return super().validate() \
            and self.__sub_validate()    
            
    def _populate_options(self) -> None:
        super()._populate_options()
        def set_input_directory_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'input_directory' and self.__input_directory is None:
                self.__input_directory = value.string_value
            else:
                raise ValueError()
            
        def set_output_dir_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'output_dir' and self.__output_dir is None:
                self.__output_dir = value.string_value
            else:
                raise ValueError()
            
        def set_colorhex_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'colorhex' and self.__colorhex is None:
                self.__colorhex = value.string_value
            else:
                raise ValueError()
            
        def set_invert_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'invert' and self.__invert is None:
                self.__invert = value.bool_value
            else:
                raise ValueError()
            
        def set_cell_invert_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'cell_invert' and self.__cell_invert is None:
                self.__cell_invert = value.bool_value
            else:
                raise ValueError()
                            
        def set_multiprocessing_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'multiprocessing' and self.__multiprocessing is None:
                self.__multiprocessing = value.bool_value
            else:
                raise ValueError()
            
        def set_reset_output_dir_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'reset_output_dir' and self.__reset_output_dir is None:
                self.__reset_output_dir = value.bool_value
            else:
                raise ValueError()    
        def set_output_width_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'output_width' and self.__output_width is None and self.__output_size is None:
                self.__output_width = value.int_value
            else:
                raise ValueError()
        def set_output_height_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'output_height' and self.__output_height is None and self.__output_size is None:
                self.__output_height = value.int_value
            else:
                raise ValueError()
        def set_output_size_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'output_size' and self.__output_size is None and self.__output_height is None and self.__output_width is None:
                self.__output_size = value.string_value
            else:
                raise ValueError()
        def set_rainbow_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'rainbow' and self.__rainbow is None:
                self.__rainbow = value.bool_value
            else:
                raise ValueError()
        def set_palettized_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'palettized' and self.__palettized is None:
                self.__palettized = value.bool_value
            else:
                raise ValueError()
                        
        self._populate_option('input_directory',command_line_parser.BaseHelpfulCommandLineOption('--input_directory The original folder containing an set of image files.',set_input_directory_cmd))
        self._populate_option('output_dir',command_line_parser.BaseHelpfulCommandLineOption('--output_dir The folder to place output files.',set_output_dir_cmd))
        self._populate_option('colorhex',command_line_parser.BaseHelpfulCommandLineOption('--colorHex The general color of output images.',set_colorhex_cmd))
        self._populate_option('invert',command_line_parser.BaseHelpfulCommandLineOption('--invert Invert The colors of the images',set_invert_cmd))
        self._populate_option('cell_invert',command_line_parser.BaseHelpfulCommandLineOption('--cell_invert Invert the colors of the cells in the images',set_cell_invert_cmd))
        self._populate_option('multiprocessing',command_line_parser.BaseHelpfulCommandLineOption('--multiprocessing Process multiple images at once',set_multiprocessing_cmd))
        self._populate_option('reset_output_dir',command_line_parser.BaseHelpfulCommandLineOption('--reset_output_dir Delete the output folder. Confirms overwriting.',set_reset_output_dir_cmd))
        self._populate_option('output_width',command_line_parser.BaseHelpfulCommandLineOption('--output_width Sets the output width.',set_output_width_cmd))
        self._populate_option('output_height',command_line_parser.BaseHelpfulCommandLineOption('--output_height Sets the output height.',set_output_height_cmd))
        self._populate_option('output_size',command_line_parser.BaseHelpfulCommandLineOption('--output_size Sets the output size (WxH or FFMPEG-compatible abbreviation).',set_output_size_cmd))
        self._populate_option('rainbow',command_line_parser.BaseHelpfulCommandLineOption(help_text='--rainbow Make this look like a infrared rainbow display!',hydrate_action=set_rainbow_cmd))
        self._populate_option('palettized',command_line_parser.BaseHelpfulCommandLineOption(help_text='--palettized Reduce this image to a 256 color image.',hydrate_action=set_palettized_cmd))        
    @property 
    def reset_output_dir(self):
        return self.__reset_output_dir
    
    @reset_output_dir.setter
    def reset_output_dir(self,reset_output_dir:str):
        self.__reset_output_dir=reset_output_dir
        
    @property
    def input_directory(self):
        return self.__input_directory
    
    @input_directory.setter
    def input_directory(self,input_directory:str):
        self.__input_directory=input_directory
        
    @property
    def output_dir(self):
        return self.__output_dir
    
    @output_dir.setter
    def output_dir(self,output_dir:str):
        self.__output_dir=output_dir
        
    @property
    def colorhex(self):
        return self.__colorhex
    
    @colorhex.setter
    def colorhex(self,colorhex:str):
        self.__colorhex=colorhex
        
    @property
    def invert(self):
        return self.__invert
    
    @invert.setter
    def invert(self,invert:bool):
        self.__invert=invert
        
    @property
    def cell_invert(self):
        return self.__cell_invert
    
    @cell_invert.setter
    def cell_invert(self,cell_invert:bool):
        self.__cell_invert=cell_invert
        
    @property
    def multiprocessing(self):
        return self.__multiprocessing
    
    @multiprocessing.setter
    def multiprocessing(self,multiprocessing:bool):
        self.__multiprocessing=multiprocessing
    
    @property
    def output_width(self):
        return self.__output_width
    @output_width.setter
    def output_width(self,output_width:int):
        self.__output_width=output_width
    @property
    def output_height(self):
        return self.__output_height
    @output_height.setter
    def output_height(self,output_height:int):
        self.__output_height=output_height
    @property
    def output_size(self) -> str:
        return self.__output_size
    @output_size.setter
    def output_size(self,output_size:str):        
        self.__output_size=output_size   
    @property
    def rainbow(self):
        return self.__rainbow
    @rainbow.setter
    def rainbow(self,rainbow:bool):
        self.__rainbow=rainbow
    @property
    def palettized(self):
        return self.__palettized
    @palettized.setter
    def palettized(self,palettized:bool):
        self.__palettized=palettized     

def subprocess_it(img_name:str,img_out_name:str,colorhex:str,invert,cell_invert,output_height:int,output_width:int,output_size:str,rainbow,palettized,ppool:list[list[subprocess.Popen]]):
    found=False    
    while not found:
        idx=0
        for pref in ppool:
            if pref[0] is None or pref[0].poll() is not None:
                subprocess_do(img_name=img_name,img_out_name=img_out_name,colorhex=colorhex,invert=invert,cell_invert=cell_invert,output_height=output_height,output_width=output_width,output_size=output_size,rainbow=rainbow,palettized=palettized,pref=pref)
                found=True
                break
            else:
                idx += 1
        time.sleep(0.1)
        
def subprocess_do(img_name:str,img_out_name:str,colorhex:str,invert,cell_invert,output_height:int,output_width:int,output_size:str,rainbow,palettized,pref:list[subprocess.Popen]):            
    args=[g for f in [[sys.executable,'image_process.py','--img_name',img_name,'--img_out_name',img_out_name],[] if colorhex is None else ['--colorhex',colorhex],[] if not rainbow else ['--rainbow'],[] if not invert else ['--invert'],[] if not cell_invert else ['--cell_invert'],[] if not palettized else ['--palettized'],[] if output_width is None else ['--output_width',str(output_width)],[] if output_height is None else ['--output_height',str(output_height)],[] if output_size is None else ['--output_size',output_size]] for g in f]    
    pref[0]=subprocess.Popen(args=args)
def drain(ppool:list[list[subprocess.Popen]]):
    found=True
    while found:
        found=False
        for pref in ppool:
            if pref[0] is not None and pref[0].poll() is None:                
                found=True
                break
        time.sleep(0.1)
        
def main(args:MultiImageCommandLineOptions):
    opath=pathlib.Path(args.output_dir)
    ipath=pathlib.Path(args.input_directory)
    if not opath.exists():
        os.mkdir(args.output_dir)
    if args.reset_output_dir:
        for entity in opath.iterdir():
            if entity.is_symlink() or entity.is_file():
                os.remove(str(entity.resolve()))
            elif entity.is_dir():
                shutil.rmtree(str(entity.resolve()))                
    else:
        for entity in opath.iterdir():
            raise Exception('Safety: Non Empty Directory while not specifying reset_output_directory.')
    ppool=[]
    for _ in range(0,os.cpu_count()**2):
        ppool.append([None])
    for input_entity in (pathlib.Path(g) for g in sorted((str(f) for f in ipath.iterdir()))):
        name=str(input_entity.relative_to(args.input_directory))        
        output=opath.joinpath(name)
        
        if not args.multiprocessing:     
            iargs=image_process.ImageProcessCommandLineArgs()
            iargs.img_name=str(input_entity)
            iargs.img_out_name=str(output)
            iargs.colorhex=args.colorhex
            iargs.invert=args.invert
            iargs.cell_invert=args.cell_invert  
            iargs.rainbow=args.rainbow    
            iargs.palettized=args.palettized      
            if args.output_size is not None:
                iargs.output_size=args.output_size
            elif args.output_height is not None and args.output_width is not None:
                iargs.output_height=args.output_height
                iargs.output_width=args.output_width                
            image_process.main(args=iargs)
        else:
            
            subprocess_it(img_name=str(input_entity),img_out_name=str(output),colorhex=args.colorhex,invert=args.invert,cell_invert=args.cell_invert,output_height=args.output_height,output_width=args.output_width,output_size=args.output_size,rainbow=args.rainbow,palettized=args.palettized,ppool=ppool)
    if args.multiprocessing:
        drain(ppool=ppool)

if __name__=='__main__':
    cp=command_line_parser.CommandLineParser()
    if cp.validate(sys.argv):                
        cp.parse_args(sys.argv)    
        bclh = MultiImageCommandLineOptionsHydrator()
        out:list[MultiImageCommandLineOptions]=[]
        ex_out:list[Exception]=[]
        if bclh.hydrate_and_validate(cp,out,ex_out):
            outx=out[0]            
            ival=outx.validate()
            if ival and not outx.help:                
                main(args=outx)
            elif not ival:
                print('Not valid args')
            
        else:
            print('Not valid args')
            traceback.print_exception(ex_out[0])
    else:
        print('Not valid args')