import subprocess
import multi_image_process
import os
import sys
import pathlib
class TempDirSet(object):
    def __init__(self) -> None:
        (self.__temp_dir,
         self.__temp_dir_out,
         self.__temp_dir_audio) = tuple([None]*3)
    @property
    def frame_split_dir(self):
        return self.__temp_dir
    @frame_split_dir.setter
    def frame_split_dir(self,frame_split_dir):
        self.__temp_dir=frame_split_dir
    @property
    def image_processing_dir(self):
        return self.__temp_dir_out
    @image_processing_dir.setter
    def image_processing_dir(self,image_processing_dir):
        self.__temp_dir_out=image_processing_dir
    @property
    def audio_output_dir(self):
        return self.__temp_dir_audio
    @audio_output_dir.setter
    def audio_output_dir(self,audio_output_dir):
        self.__temp_dir_audio = audio_output_dir    
        
        
def create_temp_dirs(movie_input_path:str,use_audio:bool):
    out=TempDirSet()
    temp_dir=f'{movie_input_path}.tmp'
    temp_dir_out=f'{movie_input_path}.otmp'
    temp_dir_audio=f'{movie_input_path}.atmp'
    os.mkdir(temp_dir)
    os.mkdir(temp_dir_out)
    if use_audio:
        os.mkdir(temp_dir_audio)
    (out.frame_split_dir,out.image_processing_dir,out.audio_output_dir) = \
    (temp_dir,temp_dir_out,temp_dir_audio)
    return out
def delete_temp_dirs(tds:TempDirSet):
    paths = (pathlib.Path(f) for f in [tds.audio_output_dir,tds.frame_split_dir,tds.image_processing_dir])
    paths = ([f] if f.exists() else [] for f in paths)
    paths = (g for f in paths for g in f)
    for f in paths:
        os.removedirs(str(f))
def split_to_frames(ffmpeg_executable_path:str,movie_input_path:str,output_movie_size:str,movie_frame_rate:float,tds:TempDirSet):
    args=[g for f in [[ffmpeg_executable_path,'-i',movie_input_path],['-s',output_movie_size] if output_movie_size is not None else [],['-r',str(movie_frame_rate)] if movie_frame_rate is not None else[],['-c:v','png','-f','image2',f'{tds.frame_split_dir}/frame_%09d.png']] for g in f]
    preprocess=subprocess.Popen(args=args,stdout=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    preprocess_code=preprocess.wait()
    return preprocess_code == 0
def extract_audio(ffmpeg_executable_path:str,movie_input_path:str,tds:TempDirSet):
    args=[g for f in [[ffmpeg_executable_path,'-i',movie_input_path,'-f','matroska','-c:a','copy','-vn',f'{tds.audio_output_dir}/audio_extract.mka']] for g in f]
    preprocess=subprocess.Popen(args=args,stdout=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    preprocess_code=preprocess.wait()
    return preprocess_code == 0   
def create_output_movie(ffmpeg_executable_path:str,movie_frame_rate:float,tds:TempDirSet,use_audio:bool,movie_output_path:str):
    args=[g for f in [[ffmpeg_executable_path,'-i',f'{tds.image_processing_dir}/frame_%09d.png'],['-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100'] if not use_audio else ['-i',f'{tds.audio_output_dir}/audio_extract.mka'],['-r',str(movie_frame_rate)] if movie_frame_rate is not None else [],['-c:v','libx264','-crf','17','-preset','veryslow','-c:a','aac','-ab','192k','-ar','44100','-ac','2','-f','mp4','-shortest',movie_output_path]] for g in f]
    preprocess=subprocess.Popen(args=args,stdout=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    preprocess_code=preprocess.wait()
    return preprocess_code == 0
def main(ffmpeg_executable_path: str,movie_input_path: str,movie_output_path: str, output_movie_size: str=None, movie_frame_rate: float=None,color_hex: str=None,invert: bool=False,cell_invert: bool=False,use_audio=False):    
    tds = create_temp_dirs(movie_input_path=movie_input_path,use_audio=use_audio)
    
    if use_audio:
        success = extract_audio(ffmpeg_executable_path=ffmpeg_executable_path,movie_input_path=movie_input_path,tds=tds)
    else:
        success = True
    if not success:
        sys.stderr.write(f'Failed in audio extraction\n')
        return 1
    success = split_to_frames(ffmpeg_executable_path=ffmpeg_executable_path,movie_input_path=movie_input_path,output_movie_size=output_movie_size,movie_frame_rate=movie_frame_rate,tds=tds)
    if not success:
        sys.stderr.write(f'Failed in movie preprocessing\n')
        return 1    
    multi_image_process.main(input_directory=tds.frame_split_dir,output_dir=tds.image_processing_dir,colorhex=color_hex,invert=invert,cell_invert=cell_invert,multiprocessing=True)
    success = create_output_movie(ffmpeg_executable_path=ffmpeg_executable_path,movie_frame_rate=movie_frame_rate,tds=tds,use_audio=use_audio,movie_output_path=movie_output_path)
    if not success:
        sys.stderr.write(f'Failed in final movie export\n')
        return 1
    delete_temp_dirs(tds=tds)
    return 0
    

if __name__=="__main__":
    argv_process=[f if len(f) > 0 else None for f in sys.argv]
    if len(argv_process) == 4:
        return_code = main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3])
    elif len(argv_process) == 5:    
        return_code = main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4])
    elif len(argv_process) == 6:
        return_code = main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4],movie_frame_rate=float(argv_process[5]) if argv_process[5] is not None else None)
    elif len(argv_process) == 7:
        return_code = main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4],movie_frame_rate=float(argv_process[5]) if argv_process[5] is not None else None,color_hex=argv_process[6])
    elif len(argv_process) == 8:
        return_code = main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4],movie_frame_rate=float(argv_process[5]) if argv_process[5] is not None else None,color_hex=argv_process[6],invert=argv_process[7].lower() in ['y','t','yes','true','1'] if argv_process[7] is not None else None)
    elif len(argv_process) == 9:
        return_code = main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4],movie_frame_rate=float(argv_process[5]) if argv_process[5] is not None else None,color_hex=argv_process[6],invert=argv_process[7].lower() in ['y','t','yes','true','1'] if argv_process[7] is not None else None,cell_invert=argv_process[8].lower() in ['y','t','yes','true','1'] if argv_process[8] is not None else None)
    elif len(argv_process) == 10:
        return_code = main(ffmpeg_executable_path=argv_process[1],movie_input_path=argv_process[2],movie_output_path=argv_process[3],output_movie_size=argv_process[4],movie_frame_rate=float(argv_process[5]) if argv_process[5] is not None else None,color_hex=argv_process[6],invert=argv_process[7].lower() in ['y','t','yes','true','1'] if argv_process[7] is not None else None,cell_invert=argv_process[8].lower() in ['y','t','yes','true','1'] if argv_process[8] is not None else None,use_audio=argv_process[9].lower() in ['y','t','yes','true','1'] if argv_process[9] is not None else None)