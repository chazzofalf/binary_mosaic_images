import PIL
import PIL.Image
import PIL.ImageDraw
import math
import sys

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
def colorize_image(img:PIL.Image,colorhex:str,invert:bool):
    if colorhex is not None and colorhex.startswith('#'):
        red=int((colorhex[1:])[:2],base=16)
        green=int((colorhex[3:])[:2],base=16)
        blue=int((colorhex[5:])[:2],base=16)
        tempimgout=PIL.Image.new('RGB',img.size)
        for y in range(0,tempimgout.height):
            for x in range(0,tempimgout.width):
                cg=img.getpixel((x,y))
                tempimgout.putpixel((x,y),(math.floor(cg*(red/256)),math.floor(cg*green/256),math.floor(cg*blue/256)))
                
        imgout=tempimgout
        imgout=imgout.convert('RGB')
    if invert:
        tempimgout=PIL.Image.new('RGB',imgout.size)
        for y in range(0,tempimgout.height):
            for x in range(0,tempimgout.width):
                tempimgout.putpixel((x,y),(256-imgout.getpixel((x,y))[0],256-imgout.getpixel((x,y))[1],256-imgout.getpixel((x,y))[2]))          
        imgout=tempimgout
    return imgout
def main(img_name:str,img_out_name:str,colorhex:str=None,invert=False,cell_invert=False):
    img=PIL.Image.open(img_name)
    img=img.convert(mode='L')
    bit_palette=[bitblock(bytex=f) for f in range(0,256)]
    bit_palette=[colorize_image(f,colorhex=colorhex,invert=invert) for f in bit_palette]
    #bit_palette[0].show()
    #bit_palette[255].show()
    #bit_palette[127].show()
    #bit_palette[128].show()
    img_map=img.resize((math.ceil(img.width/5),math.ceil(img.height/5)))
    #img_map.show()
    #img.save('___.png')
    #(img_width,img_height)=(img.width,img.height)
    # lookup=[]
    # anti_lookup=[]
    # (img_sectors_max_x,img_sectors_max_y)=(math.ceil(img_width/5),math.ceil(img_height/5))
    imgout=PIL.Image.new('RGB',img.size)
    #drawout=PIL.ImageDraw.Draw(imgout)
    for y in range(0,img_map.height):
        for x in range(0,img_map.width):
            imgout.paste(im=bit_palette[img_map.getpixel((x,y))],box=(x*5,y*5))
            #drawout.bitmap((x*5,y*5),bit_palette[img_map.getpixel((x,y))])            
    
    # for y in range(0,img_sectors_max_y):
    #     lookup.append([])
    #     anti_lookup.append([])
    #     for x in range(0,img_sectors_max_x):
    #         if isinstance(lookup[-1],list) and isinstance(anti_lookup[-1],list):
    #             lookup[-1].append(sum((get_pixel(x*5+xd,y*5+yd,img) for yd in range(0,5) for xd in range(0,5)))//25)
    #             anti_lookup[-1].append(255-lookup[-1][-1])            
    # imgout=PIL.Image.new('L',img.size)                
    # for y in range(0,img.height):
    #     for x in range(0,img.width):
    #         try:
    #             imgout.putpixel((x,y),get_processed_pixel_color(x,y,lookup,anti_lookup) if not cell_invert else 255-get_processed_pixel_color(x,y,lookup,anti_lookup))
    #         except Exception as e:
    #             print(f'x:{x} y:{y}')
    #             raise e
    
    # if colorhex is not None and colorhex.startswith('#'):
    #     red=int((colorhex[1:])[:2],base=16)
    #     green=int((colorhex[3:])[:2],base=16)
    #     blue=int((colorhex[5:])[:2],base=16)
    #     tempimgout=PIL.Image.new('RGB',imgout.size)
    #     for y in range(0,tempimgout.height):
    #         for x in range(0,tempimgout.width):
    #             cg=imgout.getpixel((x,y))
    #             tempimgout.putpixel((x,y),(math.floor(cg*(red/256)),math.floor(cg*green/256),math.floor(cg*blue/256)))
                
    #     imgout=tempimgout
    #     imgout=imgout.convert('RGB')
    # if invert:
    #     tempimgout=PIL.Image.new('RGB',imgout.size)
    #     for y in range(0,tempimgout.height):
    #         for x in range(0,tempimgout.width):
    #             tempimgout.putpixel((x,y),(256-imgout.getpixel((x,y))[0],256-imgout.getpixel((x,y))[1],256-imgout.getpixel((x,y))[2]))          
    #     imgout=tempimgout
    #imgout.show()
    imgout.save(img_out_name)
    
if __name__=='__main__':
    if len(sys.argv) == 3:
        main(img_name=sys.argv[1],img_out_name=sys.argv[2])
    elif len(sys.argv) == 4:
        main(img_name=sys.argv[1],img_out_name=sys.argv[2],colorhex=sys.argv[3] if len(sys.argv[3]) > 0 else None)
    elif len(sys.argv) == 5:
        main(img_name=sys.argv[1],img_out_name=sys.argv[2],colorhex=sys.argv[3] if len(sys.argv[3]) > 0 else None,invert=sys.argv[4].lower() in ['y','t','yes','true','1'] if len(sys.argv[4]) > 0 else None)
    elif len(sys.argv) == 6:
        main(img_name=sys.argv[1],img_out_name=sys.argv[2],colorhex=sys.argv[3] if len(sys.argv[3]) > 0 else None,invert=sys.argv[4].lower() in ['y','t','yes','true','1'] if len(sys.argv[4]) > 0 else None,cell_invert=sys.argv[5].lower() in ['y','t','yes','true','1'] if len(sys.argv[5]) > 0 else None)
        
