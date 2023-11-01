import PIL
import PIL.Image
import os
import pathlib
import math
import sys
# Requirements (Output of python -m pip freeze) (everything between the ''' lines):
# Everything contained in one file for easy posting! 😁🦋
'''
Pillow==10.1.0

'''
class ImageProcessing(object):
    def __init__(self) -> None:
        pass
    def get_pixel(self,x: int, y: int,img: PIL.Image.Image):
        return img.getpixel((x % img.width,y % img.height))
    def get_sector_pixel(self,x: int, y: int,lookup: list):    
        return lookup[y//5][x//5]
    def get_sector_bit(self,x: int, y: int,lookup: list):
        return 1 if self.get_sector_pixel(x,y,lookup) >= 128 else 0
    def get_sector_anti_pixel(self,x: int, y: int,anti_lookup: list):
        return anti_lookup[y//5][x//5]
    def is_in_text(self,x: int, y: int,lookup: list):
        return (
            self.get_sector_bit(x,y,lookup) == 0 and (
                (y % 5 in (1,3) and x % 5  >= 1 and x % 5 <= 3) or (
                    y % 5 == 2 and x % 5 in (1,3)
                )
            )
        ) or (
            self.get_sector_bit(x,y,lookup) == 1 and (
                x % 5 == 2 and y % 5 >= 1 and y % 5 <= 3
            )
        )
    def get_processed_pixel_color(self,x: int, y: int,lookup: list,anti_lookup:list):
        if self.is_in_text(x,y,lookup):
            return self.get_sector_anti_pixel(x,y,anti_lookup)
        else:
            return self.get_sector_pixel(x,y,lookup)
    def process(self,img_name:str,img_out_name:str,colorhex:str=None,invert=False,cell_invert=False):
        img=PIL.Image.open(img_name)
        img=img.convert(mode='L')
        #img.save('___.png')
        (img_width,img_height)=(img.width,img.height)
        lookup=[]
        anti_lookup=[]
        (img_sectors_max_x,img_sectors_max_y)=(math.ceil(img_width/5),math.ceil(img_height/5))
        for y in range(0,img_sectors_max_y):
            lookup.append([])
            anti_lookup.append([])
            for x in range(0,img_sectors_max_x):
                if isinstance(lookup[-1],list) and isinstance(anti_lookup[-1],list):
                    lookup[-1].append(sum((self.get_pixel(x*5+xd,y*5+yd,img) for yd in range(0,5) for xd in range(0,5)))//25)
                    anti_lookup[-1].append(255-lookup[-1][-1])    
        
        imgout=PIL.Image.new('L',img.size)
        for y in range(0,img.height):
            for x in range(0,img.width):
                try:
                    imgout.putpixel((x,y),self.get_processed_pixel_color(x,y,lookup,anti_lookup) if not cell_invert else 255-self.get_processed_pixel_color(x,y,lookup,anti_lookup))
                except Exception as e:
                    print(f'x:{x} y:{y}')
                    raise e
        
        if colorhex is not None and colorhex.startswith('#'):
            red=int((colorhex[1:])[:2],base=16)
            green=int((colorhex[3:])[:2],base=16)
            blue=int((colorhex[5:])[:2],base=16)
            tempimgout=PIL.Image.new('RGB',imgout.size)
            for y in range(0,tempimgout.height):
                for x in range(0,tempimgout.width):
                    cg=imgout.getpixel((x,y))
                    tempimgout.putpixel((x,y),(math.floor(cg*(red/256)),math.floor(cg*green/256),math.floor(cg*blue/256)))
                    
            imgout=tempimgout
            imgout=imgout.convert('RGB')
        if invert:
            tempimgout=PIL.Image.new('RGB',imgout.size)
            for y in range(0,tempimgout.height):
                for x in range(0,tempimgout.width):
                    tempimgout.putpixel((x,y),(256-imgout.getpixel((x,y))[0],256-imgout.getpixel((x,y))[1],256-imgout.getpixel((x,y))[2]))          
            imgout=tempimgout
        imgout.save(img_out_name)
        
class MultiImageProcessing(object):
    def process(self,input_directory: str,output_dir: str,reset_output_dir: bool=False,colorhex:str=None,invert=False,cell_invert=False):
        im=ImageProcessing()
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
            im.process(img_name=str(input_entity),img_out_name=str(output),colorhex=colorhex,invert=invert,cell_invert=cell_invert)
            
if __name__ == "__main__":
    if len(sys.argv) == 3:
        if pathlib.Path(sys.argv[1]).is_file():
            ip=ImageProcessing()
            ip.process(img_name=sys.argv[1],img_out_name=sys.argv[2])
        else:
            ip=MultiImageProcessing()
            ip.process(input_directory=sys.argv[1],output_dir=sys.argv[2])
    elif len(sys.argv) == 4:
        if pathlib.Path(sys.argv[1]).is_file():
            ip=ImageProcessing()
            ip.process(img_name=sys.argv[1],img_out_name=sys.argv[2],colorhex=sys.argv[3])
        else:
            ip=MultiImageProcessing()
            ip.process(input_directory=sys.argv[1],output_dir=sys.argv[2],colorhex=sys.argv[3])        
    elif len(sys.argv) == 5:
        if pathlib.Path(sys.argv[1]).is_file():
            ip=ImageProcessing()
            ip.process(img_name=sys.argv[1],img_out_name=sys.argv[2],colorhex=sys.argv[3],cell_invert=sys.argv[4].lower() in ['y','t','yes','true','1'])
        else:
            ip=MultiImageProcessing()
            ip.process(input_directory=sys.argv[1],output_dir=sys.argv[2],colorhex=sys.argv[3],cell_invert=sys.argv[4].lower() in ['y','t','yes','true','1'])         