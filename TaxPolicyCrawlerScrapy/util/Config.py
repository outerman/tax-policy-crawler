import configparser
import os
import sys
import traceback

conf = None


def get_system_conf():
    global conf
    if not conf:
        try:
            conf = configparser.ConfigParser()
            # 执行路径，debug时python的路径，打包成exe是exe的路径
            exe_running_path = os.path.dirname(sys.executable)
            exe_path = os.path.dirname(sys.argv[0])
            printf("执行路径：" + exe_running_path)
            printf("exe所在路径：" + exe_path)
            config_file = exe_path + "\\system.ini"
            if not os.path.exists(config_file):
                config_file = exe_running_path + "\\system.ini"
            printf("读取配置文件：" + config_file)
            conf.read(config_file, 'utf-8')
        except Exception as e:
            print(traceback.format_exc())
    return conf


def get_conf(filename):
    conf = configparser.ConfigParser()
    # 执行路径，debug时python的路径，打包成exe是exe的路径
    exe_running_path = os.path.dirname(sys.executable)
    exe_path = os.path.dirname(sys.argv[0])
    printf("执行路径：" + exe_running_path)
    printf("exe所在路径：" + exe_path)
    config_file = exe_path + "\\" + filename
    if not os.path.exists(config_file):
        config_file = exe_running_path + "\\" + filename
    printf("读取配置文件：" + config_file)
    conf.read(config_file, 'utf-8')


def printf(msg):
    print("[RobotConfig] " + str(msg), flush=True)


class ConstantConfig:
    def __init__(self, config_file):
        self.conf = configparser.ConfigParser()
        self.conf.read(config_file, 'utf-8')

    def get_constant(self, cons_name):
        return self.conf.get('constants', cons_name)

    def get_point(self, conf_name):
        return self.conf.get('points', conf_name)

    def get_number(self, conf_name):
        return self.conf.getint('number', conf_name)
