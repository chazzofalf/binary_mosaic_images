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
    def __fill_autos(self):
        self.__invert = False if self.__invert is None else self.__invert
        self.__cell_invert = False if self.__cell_invert is None else self.__cell_invert
        self.__multiprocessing = False if self.__multiprocessing is None else self.__multiprocessing
        self.__reset_output_dir = False if self.__reset_output_dir is None else self.__reset_output_dir        
    def __sub_validate(self) -> bool:
        self.__fill_autos()
        return self.__input_directory is not None \
            and self.__output_dir is not None
    
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
        self._populate_option('input_directory',command_line_parser.BaseHelpfulCommandLineOption('--input_directory The original folder containing an set of image files.',set_input_directory_cmd))
        self._populate_option('output_dir',command_line_parser.BaseHelpfulCommandLineOption('--output_dir The folder to place output files.',set_output_dir_cmd))
        self._populate_option('colorhex',command_line_parser.BaseHelpfulCommandLineOption('--colorHex The general color of output images.',set_colorhex_cmd))
        self._populate_option('invert',command_line_parser.BaseHelpfulCommandLineOption('--invert Invert The colors of the images',set_invert_cmd))
        self._populate_option('cell_invert',command_line_parser.BaseHelpfulCommandLineOption('--cell_invert Invert the colors of the cells in the images',set_cell_invert_cmd))
        self._populate_option('multiprocessing',command_line_parser.BaseHelpfulCommandLineOption('--multiprocessing Process multiple images at once',set_multiprocessing_cmd))
        self._populate_option('reset_output_dir',command_line_parser.BaseHelpfulCommandLineOption('--reset_output_dir Delete the output folder. Confirms overwriting.',set_reset_output_dir_cmd))
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
        


def subprocess_it(img_name:str,img_out_name:str,colorhex:str,invert,cell_invert,ppool:list[list[subprocess.Popen]]):
    found=False    
    while not found:
        idx=0
        for pref in ppool:
            if pref[0] is None or pref[0].poll() is not None:
                subprocess_do(img_name=img_name,img_out_name=img_out_name,colorhex=colorhex,invert=invert,cell_invert=cell_invert,pref=pref)
                found=True
                #print(f'{idx}/{len(ppool)}')
                break
            else:
                idx += 1
        time.sleep(0.1)
def subprocess_do(img_name:str,img_out_name:str,colorhex:str,invert,cell_invert,pref:list[subprocess.Popen]):            
    args=[g for f in [[sys.executable,'image_process.py','--img_name',img_name,'--img_out_name',img_out_name],[] if colorhex is None else ['--colorhex',colorhex],[] if not invert else ['--invert'],[] if not cell_invert else ['--cell_invert']] for g in f]    
    pref[0]=subprocess.Popen(args=args)
    #print('Process Executing...')
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
    for input_entity in ipath.iterdir():
        name=str(input_entity.relative_to(args.input_directory))        
        output=opath.joinpath(name)
        if not args.multiprocessing:     
            iargs=image_process.ImageProcessCommandLineArgs()
            iargs.img_name=str(input_entity)
            iargs.img_out_name=str(output)
            iargs.colorhex=args.colorhex
            iargs.invert=args.invert
            iargs.cell_invert=args.cell_invert
            image_process.main(args=iargs)
        else:
            subprocess_it(img_name=str(input_entity),img_out_name=str(output),colorhex=args.colorhex,invert=args.invert,cell_invert=args.cell_invert,ppool=ppool)
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
            if outx.validate() and not outx.help:                
                main(args=outx)
        else:
            print('Not valid args')
            traceback.print_exception(ex_out[0])
    else:
        print('Not valid args')