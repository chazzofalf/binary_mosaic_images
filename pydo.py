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
    tmpsrc=str(pathlib.Path('/temp/in/' + docker_args['IMG_NAME']))
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
    tmpsrc=str(pathlib.Path('/temp/in/' + docker_args['INPUT_DIRECTORY']))
    tmpdest=str(pathlib.Path('/temp/out/' + docker_args['OUTPUT_DIR']))
    dest=str(pathlib.Path('/output/' + docker_args['OUTPUT_DIR']))
    if (pathlib.Path(dest).exists()):
        raise Exception(f'Destination path exists. Please move the preexisting file that is located at {dest} to somewhere else safe to continue. Safely Bailing...')
    shutil.copytree(src=src,dst=tmpsrc)
    args.extend(('--input_directory',tmpsrc))
    args.extend(('--output_dir',tmpdest))
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
    tmpsrc=str(pathlib.Path('/temp/in/' + docker_args['MOVIE_INPUT_PATH']))
    tmpdest=str(pathlib.Path('/temp/out/' + docker_args['MOVIE_OUTPUT_PATH']))
    dest=str(pathlib.Path('/output/' + docker_args['MOVIE_OUTPUT_PATH']))
    if (pathlib.Path(dest).exists()):
        raise Exception(f'Destination path exists. Please move the preexisting file that is located at {dest} to somewhere else safe to continue. Safely Bailing...')    
    shutil.copy(str(src),str(tmpsrc))
    args.extend(('--movie_input_path',tmpsrc))
    args.extend(('--movie_output_path',tmpdest))
    checkkeys_full=(('COLOR_HEX','--color_hex'),('FFMPEG_EXECUTABLE_PATH','--ffmpeg_executable_path'),
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
else:
    help_str="""
No mode (DOCKER_EXT_ARG_MODE) was supplied so help is being given.

This docker image is driven the usage of supplied environment variables and volume mappings.
Volume Mappings (-v ...):
    -v /.../external_inputdir:/input mapping for the folder where your input file/folder exists in
    -v /.../external_outputdir:/output mapping for the folder for your output file/folder to be generated in

Environment Variables (-e DOCKER_EXT_ARG_...=...)
    All supplied environment variables that are used here are prefixed with DOCKER_EXT_ARG_
    For example., if you want a MODE of "image" you would supply -e DOCKER_EXT_ARG_MODE=image as one of the arguments applied to executing of the docker image.

    Modes (DOCKER_EXT_ARG_MODE)
        "image": Image processing mode
            Input File (DOCKER_EXT_ARG_IMG_NAME=...) Required
            Output File (DOCKER_EXT_ARG_IMG_OUT_NAME=...) Required
            Shade color (DOCKER_EXT_ARG_COLORHEX='#RRGGBB') Optional
                RGB are hexadecimal numbers. Remember to enclose the value in 'single quotes' otherwise the shell will interpret the # as a comment.
            Output Width (DOCKER_EXT_ARG_OUTPUT_WIDTH=<integer>) Optional
            Output Height (DOCKER_EXT_ARG_OUTPUT_HEIGHT=<integer>) Optional
            Output Size  (DOCKER_EXT_ARG_OUTPUT_SIZE=...) Optional
                Either in WxH format or an size abbreviation (such as ntsc). List of abbreviations is found at the end.
            Invert Colors (DOCKER_EXT_ARG_OUTPUT_INVERT=y) Optional
            Invert Colors (DOCKER_EXT_ARG_OUTPUT_CELL_INVERT=y) Optional
            Rainbow Colors (DOCKER_EXT_ARG_OUTPUT_RAINBOW=y) Optional
            256 most closest Colors (DOCKER_EXT_ARG_OUTPUT_PALETTIZED=y) Optional
        "folder": Folder Processing mode
            Input Directory (DOCKER_EXT_ARG_INPUT_DIRECTORY=...) Required
            Output Directory (DOCKER_EXT_ARG_OUTPUT_DIR=...) Required
            Shade color (DOCKER_EXT_ARG_COLORHEX='#RRGGBB') Optional
                RGB are hexadecimal numbers. Remember to enclose the value in 'single quotes' otherwise the shell will interpret the # as a comment.
            Output Width (DOCKER_EXT_ARG_OUTPUT_WIDTH=<integer>) Optional
            Output Height (DOCKER_EXT_ARG_OUTPUT_HEIGHT=<integer>) Optional
            Output Size  (DOCKER_EXT_ARG_OUTPUT_SIZE=...) Optional
                Either in WxH format or an size abbreviation (such as ntsc). List of abbreviations is found at the end.
            Invert Colors (DOCKER_EXT_ARG_OUTPUT_INVERT=y) Optional
            Invert Colors (DOCKER_EXT_ARG_OUTPUT_CELL_INVERT=y) Optional
            Rainbow Colors (DOCKER_EXT_ARG_OUTPUT_RAINBOW=y) Optional
            256 most closest Colors (DOCKER_EXT_ARG_OUTPUT_PALETTIZED=y) Optional
            Multiprocessing (DOCKER_EXT_ARG_MULTIPROCESSING=y) Optional
                Run the individual single image conversion tasks as separate processes to hopefully save some time.
        "movie": Movie Processing mode
            Input File (DOCKER_EXT_ARG_MOVIE_INPUT_PATH=...) Required
            Output File (DOCKER_EXT_ARG_MOVIE_OUTPUT_PATH=...) Required
            FFMPEG Executable Path (DOCKER_EXT_ARG_FFMPEG_EXECUTABLE_PATH=$(which ffmpeg)) DO NOT SET
                This is set by the container to use Debian's (sid) supplied ffmpeg ("apt install ffmpeg" was ran during the docker image build process) 
            Shade color (DOCKER_EXT_ARG_COLOR_HEX='#RRGGBB') Optional
                RGB are hexadecimal numbers. Remember to enclose the value in 'single quotes' otherwise the shell will interpret the # as a comment.
            Output Width (DOCKER_EXT_ARG_OUTPUT_WIDTH=<integer>) Optional
            Output Height (DOCKER_EXT_ARG_OUTPUT_HEIGHT=<integer>) Optional
            Output Size  (DOCKER_EXT_ARG_OUTPUT_SIZE=...) Optional
                Either in WxH format or an size abbreviation (such as ntsc). List of abbreviations is found at the end.
            Invert Colors (DOCKER_EXT_ARG_OUTPUT_INVERT=y) Optional
            Invert Colors (DOCKER_EXT_ARG_OUTPUT_CELL_INVERT=y) Optional
            Rainbow Colors (DOCKER_EXT_ARG_OUTPUT_RAINBOW=y) Optional
            256 most closest Colors (DOCKER_EXT_ARG_OUTPUT_PALETTIZED=y) Optional
            Framerate (fps) (DOCKER_EXT_ARG_MOVIE_FRAME_RATE=<float/integer>)
            Include Original Audio instead of silence (DOCKER_EXT_ARG_USE_AUDIO=y)                                

!!! A GENERAL WORD OF WARNING !!!
If you are going to insist on using this to "play" with other people's videos or images, please be respectful of those people's rights before attempting to publically distribute anything you generate with this app (this includes sending stuff out to your friends.)
I do not want any hurt feelings or ruined days for anyone. You have been duly warned.
G'day and Be Safe.                     
"""