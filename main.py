from Muice import Muice
from onebot import QQBotFlaskApp
import json,logging,os,traceback

logging.basicConfig(level=logging.INFO)
logging.info('在09.10更新中, 将使用(QQ号).json的方式来存储聊天记录, 对于重新拉取的源码， 可能会出现记忆缺失的情况, 对此, 请手动重命名memory下的chat_memory.json文件, 以便恢复记忆')

try:
    #使用API模式调用模型
    # from llm.api import ModelS
    # model = Model('https://127.0.0.1:8000')
    # 使用本地模式调用模型
    # 加载Qlora微调的qwen-7B模型
    # from llm.qwen import Model
    # model = Model('./model/Muice')
    from llm.chatglm2 import Model
    if os.path.exists('model/chatglm2-6b'):
        model = Model('model/chatglm2-6b','model/Muice')
        logging.info('加载chatglm2-6b模型')
    else:
        model = Model('model/chatglm2-6b-int4','model/Muice')
        logging.info('加载chatglm2-6b-int4模型')
except OSError:
    logging.error('模型加载失败, 请检查是否在model目录下放置了初始模型与微调模型')
    traceback.print_exc()
    exit()
except:
    logging.error('模型加载失败！相关报错信息如下:')
    traceback.print_exc()
    exit()

configs = json.load(open('configs.json','r',encoding='utf-8'))

muice_app = Muice(model, configs['read_memory_from_file'], configs['known_topic_probability'], configs['time_topic_probability'])
qqbot_app = QQBotFlaskApp(muice_app, configs['Trust_QQ_list'], configs['AutoCreateTopic'], configs['send_post'])  
qqbot_app.run(host = '127.0.0.1', port = configs['accept_post'])