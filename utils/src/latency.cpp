#include <dnndk/dnndk.h>
#include "dputils.h"
#include <opencv2/opencv.hpp>

int main(int argc, char *argv[]) {
    setenv("DPU_COMPILATIONMODE", "1", 1);
    //// 1.open dpu.
    int open_dpu_flag = dpuOpen();
    if (open_dpu_flag != 0) {
        std::cout << "Fail to open DPU device." << std::endl; 
    }
    //// 2.load dpu model kernel.
    DPUKernel *kernel = dpuLoadKernel(argv[1]);
    //// 3.create dpu task.
    DPUTask *task = dpuCreateTask(kernel, 1);
    //// 4.run dpu task.
    for(int i = 0; i < std::atoi(argv[2]); ++i) {
        int run_dpu_flag = dpuRunTask(task);
        if (run_dpu_flag != 0) {
            std::cout << "Fail to run DPU task." << std::endl;
        }
    }
    return 0;
}