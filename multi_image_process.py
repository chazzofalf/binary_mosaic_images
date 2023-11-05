import image_process
import os
import pathlib
import sys
import subprocess
import time
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
    pref[0]=subprocess.Popen(args=[sys.executable,'image_process.py',img_name,img_out_name,colorhex if colorhex is not None else '','y' if invert else 'n','y' if cell_invert else 'n'])
    #print('Process Executing...')
def drain(ppool:list[list[subprocess.Popen]]):
    found=True
    while found:
        found=False
        for pref in ppool:
            if pref[0] is None or pref[0].poll() is not None:                
                found=True
                break
        time.sleep(0.1)
def main(input_directory: str,output_dir: str,reset_output_dir: bool=False,colorhex:str=None,invert=False,cell_invert=False,multiprocessing=False):
    opath=pathlib.Path(output_dir)
    ipath=pathlib.Path(input_directory)
    if not opath.exists():
        os.mkdir(output_dir)
    if reset_output_dir:
        for entity in opath.iterdir():
            if entity.is_symlink() or entity.is_file():
                os.remove(str(entity.resolve()))
            elif entity.is_dir():
                os.removedirs(str(entity.resolve()))
    else:
        for entity in opath.iterdir():
            raise Exception('Safety: Non Empty Directory while not specifying reset_output_directory.')
    ppool=[]
    for _ in range(0,os.cpu_count()):
        ppool.append([None])
    for input_entity in ipath.iterdir():
        name=str(input_entity.relative_to(input_directory))        
        output=opath.joinpath(name)
        if not multiprocessing:        
            image_process.main(img_name=str(input_entity),img_out_name=str(output),colorhex=colorhex,invert=invert,cell_invert=cell_invert)    
        else:
            subprocess_it(img_name=str(input_entity),img_out_name=str(output),colorhex=colorhex,invert=invert,cell_invert=cell_invert,ppool=ppool)
    if multiprocessing:
        drain(ppool=ppool)

if __name__=='__main__':
    if len(sys.argv) == 3:
        main(input_directory=sys.argv[1],output_dir=sys.argv[2])
    elif len(sys.argv) == 4:
        main(input_directory=sys.argv[1],output_dir=sys.argv[2],colorhex=sys.argv[3])
    elif len(sys.argv) == 5:
        main(input_directory=sys.argv[1],output_dir=sys.argv[2],colorhex=sys.argv[3],invert=sys.argv[4].lower() in ['y','t','yes','true','1'],cell_invert=sys.argv[5].lower() in ['y','t','yes','true','1'])
    elif len(sys.argv) == 6:
        main(input_directory=sys.argv[1],output_dir=sys.argv[2],colorhex=sys.argv[3],invert=sys.argv[4].lower() in ['y','t','yes','true','1'],cell_invert=sys.argv[5].lower() in ['y','t','yes','true','1'],multiprocessing=sys.argv[6].lower() in ['y','t','yes','true','1'])