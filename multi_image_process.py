import image_process
import os
import pathlib
import sys
def main(input_directory: str,output_dir: str,reset_output_dir: bool=False,colorhex:str=None,invert=False,cell_invert=False):
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
    for input_entity in ipath.iterdir():
        name=str(input_entity.relative_to(input_directory))        
        output=opath.joinpath(name)
        image_process.main(img_name=str(input_entity),img_out_name=str(output),colorhex=colorhex,invert=invert,cell_invert=cell_invert)

if __name__=='__main__':
    if len(sys.argv) == 3:
        main(input_directory=sys.argv[1],output_dir=sys.argv[2])
    elif len(sys.argv) == 4:
        main(input_directory=sys.argv[1],output_dir=sys.argv[2],colorhex=sys.argv[3])
    elif len(sys.argv) == 5:
        main(input_directory=sys.argv[1],output_dir=sys.argv[2],colorhex=sys.argv[3],cell_invert=sys.argv[4].lower() in ['y','t','yes','true','1'])
