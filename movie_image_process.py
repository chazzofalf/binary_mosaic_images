import subprocess
import multi_image_process
import os
import sys
import pathlib
import shutil
import command_line_parser
import traceback
class MovieImageProcessCommandLineOptionsHydrator(command_line_parser.BaseHelpfulCommandLineHydrator):
    def __init__(self) -> None:
        super().__init__()
    def _createOptions(self):
        return MovieImageProcessCommandLineOptions()
class MovieImageProcessCommandLineOptions(command_line_parser.BaseHelpfulCommandLineOptions):
    def __init__(self) -> None:
        super().__init__()
        self.__ffmpeg_executable_path:str=None
        self.__movie_input_path:str=None
        self.__movie_output_path:str=None
        self.__output_movie_size:str=None
        self.__movie_frame_rate:float=None
        self.__color_hex:str=None
        self.__invert:bool=None
        self.__cell_invert:bool=None
        self.__use_audio:bool=None
        self.__overwrite_video:bool=None
        self.__output_width:int=None
        self.__output_height:int=None
        self.__output_size:str=None
        
    def __fill_autos(self):
        self.__invert = False if self.__invert is None else self.__invert
        self.__cell_invert = False if self.__cell_invert is None else self.__cell_invert
        self.__use_audio = False if self.__use_audio is None else self.__use_audio
        self.__overwrite_video = False if self.__overwrite_video is None else self.__overwrite_video   
             
    def __sub_validate(self):
        self.__fill_autos()
        return self.__ffmpeg_executable_path is not None and \
            self.__movie_input_path is not None and \
                self.__movie_output_path is not None and \
                    (( self.__output_size is None and self.__output_height is None and self.__output_width is None) or \
                    (self.__output_size is None and self.__output_height is not None and self.__output_width is not None) or \
                    (self.__output_size is not None and self.__output_height is None and self.__output_width is None)
                     )
                
    def _populate_options(self):
        def set_ffmpeg_executable_path_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'ffmpeg_executable_path' and self.__ffmpeg_executable_path is None:
                self.__ffmpeg_executable_path=value.string_value
            else:
                raise ValueError()      
                 
        def set_movie_input_path_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'movie_input_path' and self.__movie_input_path is None:
                self.__movie_input_path=value.string_value
            else:
                raise ValueError()  
                                     
        def set_movie_output_path_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'movie_output_path' and self.__movie_output_path is None:
                self.__movie_output_path=value.string_value
            else:
                raise ValueError()
            
        def set_output_movie_size_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'output_movie_size' and self.__output_movie_size is None:
                self.__output_movie_size=value.string_value
            else:
                raise ValueError()
            
        def set_movie_frame_rate_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'movie_frame_rate' and self.__movie_frame_rate is None:
                self.__movie_frame_rate=value.float_value
            else:
                raise ValueError()
            
        def set_color_hex_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'color_hex' and self.__color_hex is None:
                self.__color_hex=value.string_value
            else:
                raise ValueError()
            
        def set_invert_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'invert' and self.__invert is None:
                self.__invert=value.bool_value
            else:
                raise ValueError()
            
        def set_cell_invert_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'cell_invert' and self.__cell_invert is None:
                self.__cell_invert=value.bool_value
            else:
                raise ValueError()
            
        def set_use_audio_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'use_audio' and self.__use_audio is None:
                self.__use_audio=value.bool_value
            else:
                raise ValueError()
            
        def set_overwrite_video_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'overwrite_video' and self.__overwrite_video is None:
                self.__overwrite_video=value.bool_value
            else:
                raise ValueError()
        def set_output_width_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'output_width' and self.__output_width is None and self.__output_size is None:
                self.__output_width = value.int_value
            else:
                raise ValueError()
        def set_output_height_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key == 'output_height' and self.__output_height is None and self.__output_size is None:
                self.__output_height = value.int_value
            else:
                raise ValueError()
        def set_output_size_cmd(key:str,value:command_line_parser.CommandLineValue):
            if key in ['output_size','output_movie_size'] and self.__output_size is None and self.__output_height is None and self.__output_width is None:
                self.__output_size = value.string_value
            else:
                raise ValueError()
            
        self._populate_option('ffmpeg_executable_path',command_line_parser.BaseHelpfulCommandLineOption('--ffmpeg_executable_path Path to the ffmpeg executable (✅Required)',set_ffmpeg_executable_path_cmd))
        self._populate_option('movie_input_path',command_line_parser.BaseHelpfulCommandLineOption('--movie_input_path Path to the input movie file (✅)(🦋Make sure the original video producer is okay with it first!) ',set_movie_input_path_cmd))
        self._populate_option('movie_output_path',command_line_parser.BaseHelpfulCommandLineOption('--movie_output_path Path to the output movie file (✅)',set_movie_output_path_cmd))
        self._populate_option('output_movie_size',command_line_parser.BaseHelpfulCommandLineOption('--output_movie_size Image size of the videos',set_output_size_cmd))
        self._populate_option('movie_frame_rate',command_line_parser.BaseHelpfulCommandLineOption('--movie_frame_rate Frame rate of the output video',set_movie_frame_rate_cmd))
        self._populate_option('color_hex',command_line_parser.BaseHelpfulCommandLineOption('--color_hex General color of the movie',set_color_hex_cmd))
        self._populate_option('invert',command_line_parser.BaseHelpfulCommandLineOption('--invert Invert the colors of the movie',set_invert_cmd))
        self._populate_option('cell_invert',command_line_parser.BaseHelpfulCommandLineOption('--cell_invert Invert the colors of the cells of the movie',set_cell_invert_cmd))
        self._populate_option('use_audio',command_line_parser.BaseHelpfulCommandLineOption('--use_audio  Use the original audio. (🦋)',set_use_audio_cmd))
        self._populate_option('overwrite_video',command_line_parser.BaseHelpfulCommandLineOption('--overwrite_video Overwrite the original video.',set_overwrite_video_cmd))
        self._populate_option('output_width',command_line_parser.BaseHelpfulCommandLineOption('--output_width Sets the output width.',set_output_width_cmd))
        self._populate_option('output_height',command_line_parser.BaseHelpfulCommandLineOption('--output_height Sets the output height.',set_output_height_cmd))
        self._populate_option('output_size',command_line_parser.BaseHelpfulCommandLineOption('--output_size Sets the output size (WxH or FFMPEG-compatible abbreviation).',set_output_size_cmd))
        
    def validate(self) -> bool:
        return super().validate() and self.__sub_validate()

    @property
    def ffmpeg_executable_path(self):
        return self.__ffmpeg_executable_path
    
    @ffmpeg_executable_path.setter
    def ffmpeg_executable_path(self,ffmpeg_executable_path:str):
        self.__ffmpeg_executable_path=ffmpeg_executable_path
        
    @property
    def movie_input_path(self):
        return self.__movie_input_path
    
    @movie_input_path.setter
    def movie_input_path(self,movie_input_path:str):
        self.__movie_input_path=movie_input_path
        
    @property
    def movie_output_path(self):
        return self.__movie_output_path
    
    @movie_output_path.setter
    def movie_output_path(self,movie_output_path:str):
        self.__movie_output_path=movie_output_path
        
    @property
    def output_movie_size(self):
        return self.__output_movie_size
    
    @output_movie_size.setter
    def output_movie_size(self,output_movie_size:str):
        self.output_size=output_movie_size
        
    @property 
    def movie_frame_rate(self):
        return self.__movie_frame_rate
    
    @movie_frame_rate.setter
    def movie_frame_rate(self,movie_frame_rate:float):
        self.__movie_frame_rate=movie_frame_rate
        
    @property
    def color_hex(self):
        return self.__color_hex
    
    @color_hex.setter
    def color_hex(self,color_hex:str):
        self.__color_hex=color_hex
        
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
    def use_audio(self):
        return self.__use_audio
    
    @use_audio.setter
    def use_audio(self,use_audio:bool):
        self.__use_audio=use_audio
        
    @property
    def overwrite_video(self):
        return self.__overwrite_video
    
    @overwrite_video.setter
    def overwrite_video(self,overwrite_video:bool):
        self.__overwrite_video = overwrite_video
        
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
        return self.__output_size
    @output_size.setter
    def output_size(self,output_size:str):        
        self.__output_size=output_size
    
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
        shutil.rmtree(str(f))
        
def split_to_frames(ffmpeg_executable_path:str,movie_input_path:str,output_movie_size:str,movie_frame_rate:float,tds:TempDirSet):
    args=[g for f in [[ffmpeg_executable_path,'-i',movie_input_path],['-r',str(movie_frame_rate)] if movie_frame_rate is not None else[],['-c:v','png','-f','image2',f'{tds.frame_split_dir}/frame_%09d.png']] for g in f]
    preprocess=subprocess.Popen(args=args,stdout=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    preprocess_code=preprocess.wait()
    return preprocess_code == 0

def extract_audio(ffmpeg_executable_path:str,movie_input_path:str,tds:TempDirSet):
    args=[g for f in [[ffmpeg_executable_path,'-i',movie_input_path,'-f','matroska','-c:a','copy','-vn',f'{tds.audio_output_dir}/audio_extract.mka']] for g in f]
    preprocess=subprocess.Popen(args=args,stdout=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    preprocess_code=preprocess.wait()
    return preprocess_code == 0   

def create_output_movie(ffmpeg_executable_path:str,movie_frame_rate:float,tds:TempDirSet,use_audio:bool,movie_output_path:str,overwrite:bool):
    args=[g for f in [[ffmpeg_executable_path],[] if movie_frame_rate is None else ['-r',str(movie_frame_rate)],['-i',f'{tds.image_processing_dir}/frame_%09d.png'],['-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100'] if not use_audio else ['-i',f'{tds.audio_output_dir}/audio_extract.mka'],['-r',str(movie_frame_rate)] if movie_frame_rate is not None else [],['-y'] if overwrite else [],['-c:v','libx264','-crf','17','-preset','veryslow','-c:a','aac','-ab','192k','-ar','44100','-ac','2','-pix_fmt','yuv420p','-f','mp4','-shortest',movie_output_path]] for g in f]
    preprocess=subprocess.Popen(args=args,stdout=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
    preprocess_code=preprocess.wait()
    return preprocess_code == 0

def main(args:MovieImageProcessCommandLineOptions):    
    tds = create_temp_dirs(movie_input_path=args.movie_input_path,use_audio=args.use_audio)    
    if args.use_audio:
        success = extract_audio(ffmpeg_executable_path=args.ffmpeg_executable_path,movie_input_path=args.movie_input_path,tds=tds)
    else:
        success = True
    if not success:
        sys.stderr.write(f'Failed in audio extraction\n')
        return 1
    success = split_to_frames(ffmpeg_executable_path=args.ffmpeg_executable_path,movie_input_path=args.movie_input_path,output_movie_size=args.output_movie_size,movie_frame_rate=args.movie_frame_rate,tds=tds)
    if not success:
        sys.stderr.write(f'Failed in movie preprocessing\n')
        return 1    
    iargs=multi_image_process.MultiImageCommandLineOptions()
    iargs.input_directory=tds.frame_split_dir
    iargs.output_dir=tds.image_processing_dir
    iargs.colorhex=args.color_hex
    iargs.invert=args.invert
    iargs.cell_invert=args.cell_invert    
    iargs.multiprocessing=True
    if args.output_size is not None:
        iargs.output_size=args.output_size
    elif args.output_height is not None and args.output_width is not None:
        iargs.output_height=args.output_height
        iargs.output_width=args.output_width
    
    multi_image_process.main(args=iargs)
    success = create_output_movie(ffmpeg_executable_path=args.ffmpeg_executable_path,movie_frame_rate=args.movie_frame_rate,tds=tds,use_audio=args.use_audio,movie_output_path=args.movie_output_path,overwrite=args.overwrite_video)
    if not success:
        sys.stderr.write(f'Failed in final movie export\n')
        return 1
    delete_temp_dirs(tds=tds)
    return 0
    
if __name__=="__main__":
    cp=command_line_parser.CommandLineParser()
    if cp.validate(sys.argv):                
        cp.parse_args(sys.argv)    
        bclh = MovieImageProcessCommandLineOptionsHydrator()
        out:list[MovieImageProcessCommandLineOptions]=[]
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