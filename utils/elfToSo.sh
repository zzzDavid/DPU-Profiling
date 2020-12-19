#/bin/bash

elfName=$1
kernelName=${elfName#dpu_}
kernelName=${kernelName%.elf}

oneName="libdpumodel"
twoName=$kernelName
threeName=".so"
modelName=$oneName$twoName$threeName

g++ -nostdlib -fPIC -shared $1 -o $modelName

