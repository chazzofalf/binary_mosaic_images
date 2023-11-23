from typing import Iterable
import PIL
import PIL.Image
import PIL.ImageDraw
import command_line_parser 
import math
import traceback
from sys import argv

class ImageProcessCommandLineArgsHydrator(command_line_parser.BaseHelpfulCommandLineHydrator):
    def __init__(self) -> None:
        super().__init__()
    def _createOptions(self):
        return ImageProcessCommandLineArgs()
class ImageProcessCommandLineArgs(command_line_parser.BaseHelpfulCommandLineOptions):
    def __init__(self):
        super().__init__()
        self.__img_name:str=None
        self.__img_out_name:str=None
        self.__colorhex:str=None
        self.__invert:bool=None
        self.__cell_invert:bool=None
        self.__output_width:int=None
        self.__output_height:int=None
        self.__common_sizes:dict[str,str]=None
        self.__common_sizes_reversed:dict[str,str]=None
        self.__rainbow:bool=None
        self.__palettized:bool=None
        self.__generate_common_sizes()
    
    def __populate_sizes(self):
        self.__common_sizes['ntsc']='720x480'
        self.__common_sizes['pal']='720x576'
        self.__common_sizes['qntsc']='352x240'
        self.__common_sizes['qpal']='352x288'
        self.__common_sizes['sntsc']='640x480'
        self.__common_sizes['spal']='768x576'
        self.__common_sizes['film']='352x240'
        self.__common_sizes['ntsc-film']='352x240'
        self.__common_sizes['sqcif']='128x96'
        self.__common_sizes['qcif']='176x144'
        self.__common_sizes['cif']='352x288'
        self.__common_sizes['4cif']='704x576'
        self.__common_sizes['16cif']='1408x1152'
        self.__common_sizes['qqvga']='160x120'
        self.__common_sizes['qvga']='320x240'
        self.__common_sizes['vga']='640x480'
        self.__common_sizes['svga']='800x600'
        self.__common_sizes['xga']='1024x768'
        self.__common_sizes['uxga']='1600x1200'
        self.__common_sizes['qxga']='2048x1536'
        self.__common_sizes['sxga']='1280x1024'
        self.__common_sizes['qsxga']='2560x2048'
        self.__common_sizes['hsxga']='5120x4096'
        self.__common_sizes['wvga']='852x480'
        self.__common_sizes['wxga']='1366x768'
        self.__common_sizes['wsxga']='1600x1024'
        self.__common_sizes['wuxga']='1920x1200'
        self.__common_sizes['woxga']='2560x1600'
        self.__common_sizes['wqsxga']='3200x2048'
        self.__common_sizes['wquxga']='3840x2400'
        self.__common_sizes['whsxga']='6400x4096'
        self.__common_sizes['whuxga']='7680x4800'
        self.__common_sizes['cga']='320x200'
        self.__common_sizes['ega']='640x350'
        self.__common_sizes['hd480']='852x480'
        self.__common_sizes['hd720']='1280x720'
        self.__common_sizes['hd1080']='1920x1080'
        self.__common_sizes['2k']='1998x1080'
        self.__common_sizes['2kscope']='2048x858'
        self.__common_sizes['4k']='4096x2160'
        self.__common_sizes['4kflat']='3996x2160'
        self.__common_sizes['4kscope']='4096x1716'
        self.__common_sizes['nhd']='640x360'
        self.__common_sizes['hqvga']='240x160'
        self.__common_sizes['wqvga']='400x240'
        self.__common_sizes['fwqvga']='432x240'
        self.__common_sizes['hvga']='480x320'
        self.__common_sizes['qhd']='960x540'
        self.__common_sizes['2kdci']='2048x1080'
        self.__common_sizes['4kdci']='4096x2160'
        self.__common_sizes['uhd2160']='3840x2160'
        self.__common_sizes['uhd4320']='7680x4320'        
    def __generate_common_sizes(self):
        class Tagged(object):
            def __init__(self,string:str,key:str) -> None:
                self.__string:str=string
                self.__key:str=key            
            @property
            def key(self):
                return self.__key
            def __str__(self):
                return self.__string
        self.__common_sizes:dict[str:str]=dict()
        self.__populate_sizes()
        def common_sizes():
            for f in self.__common_sizes.keys():
                if isinstance(f,str):
                    value=self.__common_sizes[f]
                    if isinstance(value,str):
                        yield Tagged(value,f)
        def firsts():
            for f in set((str(f) for f in common_sizes())):
                for g in common_sizes():
                    if f == str(g):
                        yield g
                        break
        def kv():
            for f in firsts():
                yield (f.key,str(f))
        def dc() -> dict[str,str]:
            out:dict[str:str]=dict(kv())
            return out
        def cast_dict() -> dict[str,str]:
            return self.__common_sizes
        
        self.__common_sizes=cast_dict()
        self.__common_sizes_reversed=dc()

        
    def __size_for_name(self,size_name:str):
        if size_name in self.__common_sizes.keys():
            return self.__common_sizes[size_name]
        else:
            return size_name
    def __name_for_size(self,size_to_be_named:str):
        if size_to_be_named in self.__common_sizes_reversed.keys():
            return self.__common_sizes_reversed[size_to_be_named]
        else:
            return size_to_be_named
    def __fill_autos(self):
        self.__invert = False if self.__invert is None else self.__invert
        self.__cell_invert = False if self.__cell_invert is None else self.__cell_invert
        self.__rainbow = False if self.__rainbow is None else self.__rainbow
    def __is_one_or_none_of(self,items:Iterable[bool]):
        found_true=False
        for f in items:
            if f:
                if not found_true:
                    found_true=True
                else:
                    return False
        return True
    def __sub_validate(self):
        self.__fill_autos()
        return self.img_name is not None and \
            self.img_out_name is not None and \
                (self.output_width is None) == (self.output_height == None) and \
                    (
                        self.__is_one_or_none_of((self.colorhex is not None,self.rainbow,self.palettized))                        
                    )
    def validate(self) -> bool:
        return super().validate() and self.__sub_validate()
    @property 
    def img_name(self):
        return self.__img_name
    @img_name.setter
    def img_name(self,img_name:str):
        self.__img_name=img_name        
    @property 
    def img_out_name(self):
        return self.__img_out_name
    @img_out_name.setter
    def img_out_name(self,img_out_name:str):
        self.__img_out_name=img_out_name
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
    def cell_invert(self,cell_invert):
        self.__cell_invert=cell_invert
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
        if self.__output_width is not None and self.__output_height is None:
            return self.__name_for_size(f'{self.output_width}x{self.output_height}')
        return None
    @output_size.setter
    def output_size(self,output_size:str):
        if output_size is not None:
            (self.__output_width,self.__output_height) = tuple((int(f) for f in self.__size_for_name(output_size).split('x')))
        else:
            (self.__output_width,self.__output_height) = (None,None)
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
    
    
    def __set_img_name(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'img_name' and self.__img_name is None:
            self.__img_name = value.string_value        
        else:
            raise ValueError()
    def __set_img_out_name_call(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'img_out_name' and self.__img_out_name is None:
            self.__img_out_name = value.string_value        
        else:
            raise ValueError()
    def __set_colorhex_call(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'colorhex' and self.__colorhex is None:
            self.__colorhex = value.string_value        
        else:
            raise ValueError()
    def __set_invert_call(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'invert' and self.__invert is None:
            self.__invert = value.bool_value        
        else:
            raise ValueError()
    def __set_cell_invert_call(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'cell_invert' and self.__cell_invert is None:
            self.__cell_invert = value.bool_value        
        else:
            raise ValueError()
    def __set_output_width_call(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'output_width' and self.__output_width is None:
            self.__output_width = value.int_value        
        else:
            raise ValueError()
    def __set_output_height_call(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'output_height' and self.__output_height is None:
            self.__output_height = value.int_value        
        else:
            raise ValueError()
    def __set_output_size_call(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'output_size' and self.__output_height is None and self.__output_width is None:
            self.output_size=value.string_value
        else:
            raise ValueError()
    def __set_rainbow_call(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'rainbow' and self.__rainbow is None:
            self.rainbow=value.bool_value
        else:
            raise ValueError()
    def __set_palettized_call(self,key:str,value:command_line_parser.CommandLineValue):
        if key == 'palettized' and self.__palettized is None:
            self.palettized=value.bool_value
        else:
            raise ValueError()
    def _populate_options(self):
        def set_img_name_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_img_name(key=key,value=value)
        def set_img_out_name_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_img_out_name_call(key=key,value=value)
        def set_colorhex_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_colorhex_call(key=key,value=value)
        def set_invert_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_invert_call(key=key,value=value)
        def set_cell_invert_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_cell_invert_call(key=key,value=value)
        def set_output_width_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_output_width_call(key=key,value=value)
        def set_output_height_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_output_height_call(key=key,value=value)
        def set_output_size_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_output_size_call(key=key,value=value)
        def set_rainbow_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_rainbow_call(key=key,value=value)
        def set_palettized_call(key:str,value:command_line_parser.CommandLineValue):
            self.__set_palettized_call(key=key,value=value)
        self._populate_option('img_name',command_line_parser.BaseHelpfulCommandLineOption(help_text='--img_name The name of the input image',hydrate_action=set_img_name_call))
        self._populate_option('img_out_name',command_line_parser.BaseHelpfulCommandLineOption(help_text='--img_out_name The name of the output image',hydrate_action=set_img_out_name_call))
        self._populate_option('colorhex',command_line_parser.BaseHelpfulCommandLineOption(help_text='--colorhex The general color of the output image',hydrate_action=set_colorhex_call))
        self._populate_option('invert',command_line_parser.BaseHelpfulCommandLineOption(help_text='--invert Whether to invert the colors of the image or not',hydrate_action=set_invert_call))
        self._populate_option('cell_invert',command_line_parser.BaseHelpfulCommandLineOption(help_text='--cell_invert Whether to invert the grayscale base of the colors of the cells within the image or not',hydrate_action=set_cell_invert_call))
        self._populate_option('output_width',command_line_parser.BaseHelpfulCommandLineOption(help_text='--output_width The width of the output',hydrate_action=set_output_width_call))
        self._populate_option('output_height',command_line_parser.BaseHelpfulCommandLineOption(help_text='--output_height The width of the output',hydrate_action=set_output_height_call))
        self._populate_option('output_size',command_line_parser.BaseHelpfulCommandLineOption(help_text='--output_size The width of the output (in WxH format or use and abbreviation [abbreviations are made to be compatible with FFMPEGs abbreviations])',hydrate_action=set_output_size_call))
        self._populate_option('rainbow',command_line_parser.BaseHelpfulCommandLineOption(help_text='--rainbow Make this look like a infrared rainbow display!',hydrate_action=set_rainbow_call))
        self._populate_option('palettized',command_line_parser.BaseHelpfulCommandLineOption(help_text='--palettized Reduce this image to a 256 color image.',hydrate_action=set_palettized_call))
def get_pixel(x: int, y: int,img: PIL.Image.Image):
    return img.getpixel((x % img.width,y % img.height))
def get_sector_pixel(x: int, y: int,lookup: list):    
    return lookup[y//5][x//5]
def get_sector_bit(x: int, y: int,lookup: list):
    return 1 if get_sector_pixel(x,y,lookup) >= 128 else 0
def get_sector_anti_pixel(x: int, y: int,anti_lookup: list):
    return anti_lookup[y//5][x//5]
def is_in_text(x: int, y: int,lookup: list):
    return (
        get_sector_bit(x,y,lookup) == 0 and (
            (y % 5 in (1,3) and x % 5  >= 1 and x % 5 <= 3) or (
                y % 5 == 2 and x % 5 in (1,3)
            )
        )
    ) or (
        get_sector_bit(x,y,lookup) == 1 and (
            x % 5 == 2 and y % 5 >= 1 and y % 5 <= 3
        )
    )
    
def get_processed_pixel_color(x: int, y: int,lookup: list,anti_lookup:list):
    if is_in_text(x,y,lookup):
        return get_sector_anti_pixel(x,y,anti_lookup)
    else:
        return get_sector_pixel(x,y,lookup)
    
def bitblock(bytex:int):
    imgo=PIL.Image.new(mode='L',size=(5,5),color=bytex)
    if bytex < 128:
        imgo.putpixel((1,1),255-bytex)
        imgo.putpixel((2,1),255-bytex)
        imgo.putpixel((3,1),255-bytex)
        imgo.putpixel((1,2),255-bytex)
        imgo.putpixel((3,2),255-bytex)
        imgo.putpixel((1,3),255-bytex)
        imgo.putpixel((2,3),255-bytex)
        imgo.putpixel((3,3),255-bytex)
    else:
        imgo.putpixel((2,1),255-bytex)
        imgo.putpixel((2,2),255-bytex)
        imgo.putpixel((2,3),255-bytex)
    return imgo
def bitblock_color(bytex:int,palapal:list[tuple[tuple[int,int,int],tuple[int,int,int],int]]):
    imgo=PIL.Image.new(mode='L',size=(5,5),color=bytex)    
    (color,anticolor,dist)=palapal[bytex]
    imgo=PIL.Image.new(mode='RGB',size=(5,5),color=color)
    
    if dist < 128:
        imgo.putpixel((1,1),anticolor)
        imgo.putpixel((2,1),anticolor)
        imgo.putpixel((3,1),anticolor)
        imgo.putpixel((1,2),anticolor)
        imgo.putpixel((3,2),anticolor)
        imgo.putpixel((1,3),anticolor)
        imgo.putpixel((2,3),anticolor)
        imgo.putpixel((3,3),anticolor)
    else:
        imgo.putpixel((2,1),anticolor)
        imgo.putpixel((2,2),anticolor)
        imgo.putpixel((2,3),anticolor)
    return imgo

def colorize_image(img:PIL.Image,colorhex:str,invert:bool,rainbow:bool):
    def invertc(color:tuple[int,int,int]) -> tuple[int,int,int]:
        def map_channel(channel:int):
            return 255-channel
        return tuple((map_channel(f) for f in color))
    def hex_to_color(hexcode:str):
        if hexcode is not None and hexcode.startswith('#'):
            red=int((hexcode[1:])[:2],base=16)
            green=int((hexcode[3:])[:2],base=16)
            blue=int((hexcode[5:])[:2],base=16)
            return (red,green,blue)
        raise ValueError()
    def colorize_gray(grayscale:int,color:tuple[int,int,int]) -> tuple[int,int,int]:
        return tuple((math.floor((grayscale/255)*f) for f in color))   
    def mix(colorA:tuple[int,int,int],colorB:tuple[int,int,int],fractB:float):
        def map_channel(channelA:int,channelB:int) -> tuple[int,int,int]:
            return math.floor(((1.0-fractB)*channelA)+(fractB*channelB))
        return tuple(map(map_channel,colorA,colorB))
    def convert_gray_to_rainbow_color(grayscale:int):
        red_color=(255,0,0)
        yellow_color=(255,255,0)
        green_color=(0,255,0)
        cyan_color=(0,255,255)
        blue_color=(0,0,255)
        magenta_color=(255,0,255)
        primaries=[blue_color,cyan_color,green_color,yellow_color,red_color,magenta_color]
        raw_index=((grayscale/255)*(len(primaries)-1))
        primary_index=math.floor(raw_index)
        fract_index=raw_index-primary_index
        if fract_index==0:
            color=primaries[primary_index]
        else:
            color=mix(primaries[primary_index],primaries[primary_index+1],fract_index)
        color=colorize_gray(grayscale,color)
        return color
    tempimgout=PIL.Image.new('RGB',img.size)            
    if colorhex is not None and colorhex.startswith('#') and not rainbow:
        colorizing_color=hex_to_color(colorhex)        
        for y in range(0,tempimgout.height):
            for x in range(0,tempimgout.width):
                cg=img.getpixel((x,y))
                color=colorize_gray(cg,colorizing_color)
                if invert:
                    color=invertc(color)
                tempimgout.putpixel((x,y),color)                        
    elif rainbow and colorhex is None:        
        tempimgout=PIL.Image.new('RGB',img.size)        
        for y in range(0,tempimgout.height):
            for x in range(0,tempimgout.width):
                cg=img.getpixel((x,y))
                color=convert_gray_to_rainbow_color(cg)
                if invert:
                    color=invertc(color)
                tempimgout.putpixel((x,y),color)
    elif not rainbow and colorhex is None:                
        for y in range(0,tempimgout.height):
            for x in range(0,tempimgout.width):
                cg=img.getpixel((x,y))
                color=colorize_gray(cg,(255,255,255))
                if invert:
                    color=invertc(color)
                tempimgout.putpixel((x,y),color)
    imgout=tempimgout
    imgout=imgout.convert('RGB')
    return imgout

def main(args:ImageProcessCommandLineArgs):
    img=PIL.Image.open(args.img_name)
    img=img.convert('RGB')
    if args.output_height is not None and args.output_width is not None:
        (w_i,h_i,w_s,h_s) = (img.width,img.height,args.output_width,args.output_height)
        (r_i,r_s) = (w_i/h_i,w_s/h_s)
        (w_o,h_o) = (w_i * (h_s/h_i),h_s) if r_s > r_i else (w_s,h_i * (w_s/w_i))
        (x_c,y_c) = (w_s/2,h_s/2)
        (x_s,y_s) = (0 if w_o == w_s else x_c-(w_o/2),0 if h_o == h_s else y_c-(h_o/2))
        (x_s,y_s,w_o,h_o) = tuple((math.floor(f) for f in (x_s,y_s,w_o,h_o)))
        rect = tuple((f for f in (x_s,y_s,x_s+w_o,y_s+h_o)))
        bimg=img.resize((math.floor(w_o),math.floor(h_o)))
        img=PIL.Image.new('RGB',(w_s,h_s))
        try:
            img.paste(bimg,rect)            
        except:
            print(f'Failed to process {args.img_name} with rect of {rect} into output of {img.size} with input of size of {bimg.size}')
            return
    if args.colorhex is not None or args.invert or args.rainbow or not args.palettized:
        img=img.convert(mode='L')
        bit_palette=[bitblock(bytex=f) for f in range(0,256)]
        bit_palette=[colorize_image(f,colorhex=args.colorhex,invert=args.invert,rainbow=args.rainbow) for f in bit_palette]
        img_map=img.resize((math.ceil(img.width/5),math.ceil(img.height/5)))
        imgout=PIL.Image.new('RGB',img.size)
        for y in range(0,img_map.height):
            for x in range(0,img_map.width):
                imgout.paste(im=bit_palette[img_map.getpixel((x,y))],box=(x*5,y*5))   
    elif args.palettized:
        img_map=img.resize((math.ceil(img.width/5),math.ceil(img.height/5)))
        img_map=img_map.convert(mode='P',dither=PIL.Image.FLOYDSTEINBERG,palette=PIL.Image.Palette.ADAPTIVE,colors=256)
        def chunk3(items:list[int]):
            def chunk3gen(items_:list[int]):
                chunk:list[int]=[]
                for i in items_:
                    chunk.append(i)
                    if len(chunk) == 3:
                        yield chunk
                        chunk=[]
            return [f for f in chunk3gen(items_=items)]
        pal=chunk3(img_map.getpalette())
        apal=[[255-g for g in f] for f in pal]
        pal=[tuple(f) for f in pal]
        apal=[tuple(f) for f in apal]
        def palapalmap(c:tuple[int,int,int],ac:tuple[int,int,int]):
            return (c,ac,math.floor(math.sqrt((c[0]**2)+(c[1]**2)+(c[2]**2))))
        palapal=[f for f in map(palapalmap,pal,apal)]
        bit_palette=[bitblock_color(bytex=f,palapal=palapal) for f in range(0,256)]
        imgout=PIL.Image.new(mode='RGB',size=(img.width,img.height))
        for y in range(0,img_map.height):
            for x in range(0,img_map.width):
                imgout.paste(im=bit_palette[img_map.getpixel((x,y))],box=(x*5,y*5)) 
    imgout.save(args.img_out_name)

if __name__=='__main__':
    cp=command_line_parser.CommandLineParser()
    if cp.validate(argv):                
        cp.parse_args(argv)    
        bclh = ImageProcessCommandLineArgsHydrator()
        out:list[ImageProcessCommandLineArgs]=[]
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
        
