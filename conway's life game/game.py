import numpy  as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import  os
plt.rcParams['animation.ffmpeg_path'] = r"D:\ffmpeg-2025-05-29-git-75960ac270-full_build\ffmpeg-2025-05-29-git-75960ac270-full_build\bin\ffmpeg.exe" # 路径需与实际一致
ON = 255
OFF = 0
vars = [ON, OFF]

def randomGrid(N):
    """随机化网格"""
    return np.random.choice([0,255], N*N, p=[0.8, 0.2]).reshape(N,N)

def addGlider(i, j, grid):
    """从位于(i, j)点的左上角细胞开始添加一架滑翔机 """
    glider = np.array([[0, 0, 255],
                      [255, 0, 255],
                      [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider

def addGosperGun(i, j, grid):
    """高斯帕滑机枪图案"""
    gun = np.zeros(11*38).reshape(11, 38)

    gun[5][1] = gun[5][2] = 255
    gun[6][1] = gun[6][2] = 255

    gun[3][13] = gun[3][14] = 255
    gun[4][12] = gun[4][16] = 255
    gun[5][11] = gun[5][17] = 255
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
    gun[7][11] = gun[7][17] = 255
    gun[8][12] = gun[8][16] = 255
    gun[9][13] = gun[9][14] = 255

    gun[1][25] = 255
    gun[2][23] = gun[2][25] = 255
    gun[3][21] = gun[3][22] = 255
    gun[4][21] = gun[4][22] = 255
    gun[5][21] = gun[5][22] = 255
    gun[6][23] = gun[6][25] = 255
    gun[7][25] = 255

    gun[3][35] = gun[3][36] = 255
    gun[4][35] = gun[4][36] = 255

    grid[i:i+11, j:j+38] = gun
    
def readPattern(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()  # 返回整个文件内容的字符串 
    arraylist = []
    for index, line in enumerate(lines):
        if  index == 0:
            number = line.split()
            N = int(number[0])
        if index != 0:
            string_list =  line.split()
            number_list = [int(num) for num in string_list]
            arraylist.append(number_list)
    grid = np.array(arraylist)
    return (N, grid)
        
        
        
def update(frameNum, N, grid, img):
    """遍历行检查单个方块周围八个方块是否符合规则，并更新网格"""
    newGrid = grid.copy()
    for j in  range(N):
        for i in range(N):
            # 遍历九宫格查找ON状态个数
            total = int((grid[i, (j+1)%N] + grid[(i-1)%N, (j+1)%N] + grid[(i+1)%N, (j+1)%N] + grid[(i-1)%N, j]
                        + grid[(i+1)%N, j] + grid[i, (j-1)%N] + grid[(i-1)%N, (j-1)%N] + grid[(i+1)%N, (j-1)%N])/255 )
            if grid[i, j] == ON:
                if (total<2) or (total>3):
                     newGrid[i, j] = OFF
            else:
                if total==3:
                    newGrid[i, j] = ON
    # 更新数据
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img


# 向程序发送命令行参数
# main（） function
def main():
    # 命令行选项
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life")

    # 添加参数
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gun', action='store_true', required=False)
    parser.add_argument('--readpattern', dest='pattern_filepath', required=False)
    args = parser.parse_args()
    
    # 设定网格大小
    N = 100
    if args.pattern_filepath:
        paras = readPattern(args.pattern_filepath)
        N = paras[0]
    elif args.N and int(args.N) > 8:                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
         N = int(args.N)
    
    # 设定动画的更新频率
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)
    
    # 声明网格
    grid = np.array([])
    # 检查滑翔机图标是否指定
    if args.pattern_filepath:
        paras = readPattern(args.pattern_filepath)
        grid = paras[1]

    elif args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1,1,grid)
    elif args.gun:
        grid = np.zeros(N*N).reshape(N, N)
        addGosperGun(1,1,grid)
    else:
         grid = randomGrid(N)
    

    # 建立动画
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation="nearest")
    ani = animation.FuncAnimation(fig, update, fargs=(N, grid, img),
                                  frames=200,
                                  interval=updateInterval,
                                  save_count=200)
    
    # 帧数？
    # 输出动画文件
     # 输出动画文件
    if args.movfile:
        try:
            # 1. 检查FFmpeg是否存在
            ffmpeg_path = plt.rcParams['animation.ffmpeg_path']
            if not os.path.exists(ffmpeg_path):
                print(f"警告: FFmpeg未找到在路径 {ffmpeg_path}")
                print("请检查FFmpeg安装路径")
            
            # 2. 确保输出目录存在
            output_dir = os.path.dirname(os.path.abspath(args.movfile))
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 3. 如果文件已存在，先删除
            if os.path.exists(args.movfile):
                try:
                    os.remove(args.movfile)
                    print(f"已删除现有文件: {args.movfile}")
                except:
                    print(f"无法删除现有文件: {args.movfile}")
            
            # 4. 尝试多种编码器
            codecs_to_try = ['libx264', 'mpeg4', 'libxvid']
            success = False
            
            for codec in codecs_to_try:
                try:
                    print(f"尝试使用 {codec} 编码器...")
                    writer = animation.FFMpegWriter(
                        fps=15,
                        bitrate=1800,
                        codec=codec,
                        extra_args=['-pix_fmt', 'yuv420p']
                    )
                    
                    ani.save(args.movfile, writer=writer, dpi=80)
                    print(f"成功使用 {codec} 编码器保存动画!")
                    success = True
                    break
                except Exception as e:
                    print(f"{codec} 编码器失败: {e}")
            
            # 5. 如果所有编码器都失败
            if not success:
                raise Exception("所有视频编码器尝试失败")
        
        # 6. 外层异常处理
        except PermissionError:
            print(f"权限错误: 无法写入文件 {args.movfile}")
            print("请尝试:")
            print("1. 以管理员身份运行程序")
            print("2. 选择不同的输出路径")
            print("3. 确保文件未被其他程序占用")
        except Exception as e:  # 正确缩进：与except PermissionError对齐
            print(f"保存动画时出错: {e}")
            print("尝试使用pillow writer作为备选方案...")
            try:
                gif_file = args.movfile.replace('.mp4', '.gif')
                ani.save(gif_file, writer='pillow', fps=10)
                print(f"已保存为GIF格式: {gif_file}")
            except Exception as e2:
                print(f"GIF保存也失败: {e2}")
    
    plt.show()
        
    

# 调用main函数
if __name__ == '__main__':
    main()

    
    
    





                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     