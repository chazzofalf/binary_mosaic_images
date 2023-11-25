import sys
import os
import pathlib
import io
import shutil
import PIL
import PIL.Image
import subprocess
extargsprefix='DOCKER_EXT_ARG_'
docker_args=dict(((h[len(extargsprefix):],os.environ[h]) for g in ([f] if f.startswith(extargsprefix) else [] for f in os.environ.keys()) for h in g))
args=[sys.executable,'-m','binary_mosaic_images']
if docker_args['MODE']=='image':
    args.append('--process-image')
    src=str(pathlib.Path('/input/' + docker_args['IMG_NAME']))
    tmpsrc=str(pathlib.Path('/temp/in/' + + docker_args['IMG_NAME']))
    tmpdest=str(pathlib.Path('/temp/out/' + docker_args['IMG_OUT_NAME']))
    dest=str(pathlib.Path('/output/' + docker_args['IMG_OUT_NAME']))
    if (pathlib.Path(dest).exists()):
        raise Exception(f'Destination path exists. Please move the preexisting file that is located at {dest} to somewhere else safe (or remove it you don\'t need it. In either case, just get it out of the way!) to continue. Safely Bailing...')
    shutil.copy(str(src),str(tmpsrc))
    args.extend(('--img_name',tmpsrc))
    args.extend(('--img_out_name',tmpdest))
    checkkeys_full=(('COLORHEX','--colorhex'),
               ('OUTPUT_WIDTH','--output_width'),('OUTPUT_HEIGHT','--output_height'),('OUTPUT_SIZE','--output_size'))
    checkkeys_flags=(('INVERT','--invert'),('CELL_INVERT','--cell_invert'),('RAINBOW','--rainbow'),('PALETTIZED','--palettized'))
    
    for f in checkkeys_full:
        (key,arg) = f
        if key in docker_args.keys():
            args.extend((arg,docker_args[key]))
    for f in checkkeys_flags:
        (key,arg) = f
        if key in docker_args.keys():
            args.append(arg)
    p=subprocess.Popen(args=args)
    p.wait()        
    shutil.copy(str(tmpdest),dest)
elif docker_args['MODE']=='folder':
    args.append('--process-folder')
    src=str(pathlib.Path('/input/' + docker_args['INPUT_DIRECTORY']))
    tmpsrc=str(pathlib.Path('/temp/in/' + + docker_args['INPUT_DIRECTORY']))
    tmpdest=str(pathlib.Path('/temp/out/' + docker_args['OUTPUT_DIR']))
    dest=str(pathlib.Path('/output/' + docker_args['OUTPUT_DIR']))
    if (pathlib.Path(dest).exists()):
        raise Exception(f'Destination path exists. Please move the preexisting file that is located at {dest} to somewhere else safe to continue. Safely Bailing...')
    shutil.copytree(src=src,dest=tmpsrc)
    args.extend(('--input_directory',tmpsrc))
    args.extend(('--out_dir',tmpdest))
    checkkeys_full=(('COLORHEX','--colorhex'),
               ('OUTPUT_WIDTH','--output_width'),('OUTPUT_HEIGHT','--output_height'),('OUTPUT_SIZE','--output_size'))
    checkkeys_flags=(('INVERT','--invert'),('CELL_INVERT','--cell_invert'),('RAINBOW','--rainbow'),('PALETTIZED','--palettized'),
                     ('MULTIPROCESSING','--multiprocessing'))
    for f in checkkeys_full:
        (key,arg) = f
        if key in docker_args.keys():
            args.extend((arg,docker_args[key]))
    for f in checkkeys_flags:
        (key,arg) = f
        if key in docker_args.keys():
            args.append(arg)
    p=subprocess.Popen(args=args)
    p.wait()   
    shutil.copytree(str(tmpdest),dest)     
elif docker_args['MODE']=='movie':
    args.append('--process-movie')
    src=str(pathlib.Path('/input/' + docker_args['MOVIE_INPUT_PATH']))
    tmpsrc=str(pathlib.Path('/temp/in/' + + docker_args['MOVIE_INPUT_PATH']))
    tmpdest=str(pathlib.Path('/temp/out/' + docker_args['MOVIE_OUTPUT_PATH']))
    dest=str(pathlib.Path('/output/' + docker_args['MOVIE_OUTPUT_PATH']))
    if (pathlib.Path(dest).exists()):
        raise Exception(f'Destination path exists. Please move the preexisting file that is located at {dest} to somewhere else safe to continue. Safely Bailing...')    
    shutil.copy(str(src),str(tmpsrc))
    args.extend(('--movie_input_path',tmpsrc))
    args.extend(('--movie_output_path',tmpdest))
    checkkeys_full=(('COLOR_HEX','--color_hex'),('FFMPEG_EXECUTABLE_PATH','--ffmpeg_executable_path')
               ('OUTPUT_WIDTH','--output_width'),('OUTPUT_HEIGHT','--output_height'),('OUTPUT_MOVIE_SIZE','--output_movie_size'),
               ('MOVIE_FRAME_RATE','--movie_frame_rate'),('OUTPUT_SIZE','--output_size'))
    checkkeys_flags=(('INVERT','--invert'),('CELL_INVERT','--cell_invert'),('RAINBOW','--rainbow'),('PALETTIZED','--palettized'),
                     ('MULTIPROCESSING','--multiprocessing'),('USE_AUDIO','--use_audio'))
    for f in checkkeys_full:
        (key,arg) = f
        if key in docker_args.keys():
            args.extend((arg,docker_args[key]))
    for f in checkkeys_flags:
        (key,arg) = f
        if key in docker_args.keys():
            args.append(arg)
    p=subprocess.Popen(args=args)
    p.wait()
    shutil.copy(str(tmpdest),dest)