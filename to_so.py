import os

def to_so():
    """
    convert all .elf to .so, 
    save it to a dir called so
    """
    elfs = os.listdir('./elf')
    so_dir = './so'
    os.mkdir(so_dir)
    for elf in elfs:
        kernel_name = elf.replace('.elf', '').split('_')[1]
        so_name = 'libdpumodel' + kernel_name + '.so'
        cmd = "g++ -nostdlib -fPIC -shared ./elf/{} -o ./so/{}".format(elf, so_name)
        print(cmd)
        os.system(cmd)

    # note: ya'll need to copy the .so files to /usr/lib
    # setting LD_LIBRARY_PATH doesn't work, I tried.    


if __name__ == "__main__":
    to_so()
