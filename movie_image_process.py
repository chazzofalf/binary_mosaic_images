import subprocess
import multi_image_process
import os
import sys
def main(ffmpeg_executable_path: str,movie_input_path: str,movie_output_path: str, output_movie_size: str=None, movie_frame_rate: float=None,color_hex: str=None,invert: bool=False,cell_invert: bool=False):    
    temp_dir=f'{movie_input_path}.tmp'
    temp_dir_out=f'{movie_input_path}.otmp'
    os.mkdir(temp_dir)
    os.mkdir(temp_dir_out)        
    args=[g for f in [[ffmpeg_executable_path,'-i',movie_input_path],['-s',output_movie_size] if output_movie_size is not None else [],['-r',str(movie_frame_rate)] if movie_frame_rate is not None else[],['-c:v','png','-f','image2',f'{temp_dir}/frame_%09d.png']] for g in f]
    preprocess=subprocess.Popen(args=args,stdout=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    preprocess_code=preprocess.wait()
    if preprocess_code == 0:
        multi_image_process.main(input_directory=temp_dir,output_dir=temp_dir_out,colorhex=color_hex,invert=invert,cell_invert=cell_invert)
        args=[g for f in [[ffmpeg_executable_path,'-i',f'{temp_dir_out}/frame_%09d.png','-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100'],['-r',str(movie_frame_rate)] if movie_frame_rate is not None else [],['-c:v','libx264','-crf','17','-preset','veryslow','-c:a','aac','-ab','192k','-ar','44100','-ac','2','-f','mp4',movie_output_path]] for g in f]
        preprocess=subprocess.Popen(args=args,stdout=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
        preprocess_code=preprocess.wait()
        if preprocess_code != 0:
            sys.stderr.write(f'Failed in movie preprocessing with exit code: {preprocess_code}\n')
        exit(preprocess_code)
    else:
        sys.stderr.write(f'Failed in movie preprocessing with exit code: {preprocess_code}\n')
        exit(preprocess_code)

if __name__=="__main__":
    argv_process=[f if len(f) > 0 else None for f in sys.argv]
    if len(argv_process) == 4:
        main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3])
    elif len(argv_process) == 5:    
        main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4])
    elif len(argv_process) == 6:
        main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4],movie_frame_rate=float(argv_process[5]) if argv_process[5] is not None else None)
    elif len(argv_process) == 7:
        main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4],movie_frame_rate=float(argv_process[5]) if argv_process[5] is not None else None,color_hex=argv_process[6])
    elif len(argv_process) == 8:
        main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4],movie_frame_rate=float(argv_process[5]) if argv_process[5] is not None else None,color_hex=argv_process[6],invert=argv_process[7].lower() in ['y','t','yes','true','1'] if argv_process[7] is not None else None)
    elif len(argv_process) == 9:
        main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4],movie_frame_rate=float(argv_process[5]) if argv_process[5] is not None else None,color_hex=argv_process[6],invert=argv_process[7].lower() in ['y','t','yes','true','1'] if argv_process[7] is not None else None,cell_invert=argv_process[8].lower() in ['y','t','yes','true','1'] if argv_process[8] is not None else None)