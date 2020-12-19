1. 自动化编译工具，生成板卡可部署的模型

   **注意:** 测试latency的模型必须为**debug**版本(模型为: debug版和normal版)

2. 编译测试latency Demo: 

   ```
   mkdir build
   cd build
   cmake ..
   make -j4
   ```

3. 步骤1，模型文件文件格式为dpu_\*.elf (例如：dpu_0_dpu0.elf)
   **注意： **记录\*(0_dpu0)的内容作为模型名称，后续作为命令行参数传给可执行文件；

4. 将dpu\_\*.elf转换为lib\*.so，并拷贝到/usr/lib路径，执行脚本：

   ```
   ./elfToSo.sh dpu_*.elf
   ```

5. 运行测试latency代码，执行脚本：

   ```
   ./build/latency 0_dpu0 100 > latency.txt
   ## $0 可执行文件名称
   ## $1 模型名称，步骤3提及
   ## $2 模型推理次数，多次推理以计算平均值
   ## $3 将latency信息重定向自定义文件
   ```