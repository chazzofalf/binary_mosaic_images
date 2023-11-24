# All lee lod -> All the Line Of Duty -> That is everything glued together as in you should be able call this script to run the others. 
# Facilitates in the converting of this to a package/application ⚙️
# Why the strange spelling? 🤫 It's a secret!

from sys import argv
import image_process
import multi_image_process
import movie_image_process

def main(args:list[str]):
    needhelp=False
    if len(args) >= 2:
        app_exec_arg=args[1]
        app_exec_args=args[2:]
        app_exec_args.insert(0,args[0])
        #print(f'App name:{app_exec_arg}\nApp args:{app_exec_args}')
        if app_exec_arg=='--process-image':
            image_process.smain(app_exec_args)
        elif app_exec_arg=='--process-folder':
            multi_image_process.smain(app_exec_args)
        elif app_exec_arg=='--process-movie':
            movie_image_process.smain(app_exec_args)
        else:
            needhelp=True
    else:
        needhelp=True
    if needhelp:
        print('Choose either --process-image, --process-folder, or --process-movie as your initial command argument')
            

if __name__=='__main__':
    main(argv)

