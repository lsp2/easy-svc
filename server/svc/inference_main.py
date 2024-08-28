import logging
import os
import soundfile

from svc.inference import infer_tool
from svc.inference.infer_tool import Svc

logging.getLogger('numba').setLevel(logging.WARNING)
chunks_dict = infer_tool.read_temp("svc/inference/chunks_temp.json")



def main(progressDict, key, spk, model_dir, audio_path_list, res_path):

    slice_db = -50 # 默认-40，嘈杂的音频可以-30，干声保留呼吸可以-50
    wav_format = 'flac' # 音频输出格式
    auto_predict_f0 = False # 语音转换自动预测音高，转换歌声时不要打开这个会严重跑调
    cluster_infer_ratio = 0# 聚类方案或特征检索占比，范围0-1，若没有训练聚类模型或特征检索则默认0即可
    feature_retrieval = False # 是否使用特征检索，如果使用聚类模型将被禁用，且cm与cr参数将会变成特征检索的索引路径与混合比例
    noice_scale = 0.4 # 噪音级别，会影响咬字和音质，较为玄学
    pad_seconds = 0.5 # 推理音频pad秒数，由于未知原因开头结尾会有异响，pad一小段静音段后就不会出现
    clip = 0 # 音频强制切片，默认0为自动切片，单位为秒/s
    lg = 0 # 两段音频切片的交叉淡入长度，如果强制切片后出现人声不连贯可调整该数值，如果连贯建议采用默认值0，单位为秒
    lgr = 0.75 # 自动音频切片后，需要舍弃每段切片的头尾。该参数设置交叉长度保留的比例，范围0-1,左开右闭
    f0p = "pm" # 选择F0预测器,可选择crepe,pm,dio,harvest,rmvpe,fcpe默认为pm(注意：crepe为原F0使用均值滤波器) 
    enhance = False # 是否使用NSF_HIFIGAN增强器,该选项对部分训练集少的模型有一定的音质增强效果，但是对训练好的模型有反面效果，默认关闭
    enhancer_adaptive_key = 0 # 使增强器适应更高的音域(单位为半音数)|默认为0

    cr_threshold = 0 # F0过滤阈值，只有使用crepe时有效. 数值范围从0-1. 降低该值可减少跑调概率，但会增加哑音

    # 浅扩散设置
    k_step = 100 # 扩散步数，越大越接近扩散模型的结果，默认100
    only_diffusion = False # 纯扩散模式，该模式不会加载sovits模型，以扩散模型推理
    shallow_diffusion = False # 是否使用浅层扩散，使用后可解决一部分电音问题，默认关闭，该选项打开时，NSF_HIFIGAN增强器将会被禁止
    
    use_spk_mix = False # 是否使用角色融合
    second_encoding = False # 二次编码，浅扩散前会对原始音频进行二次编码，玄学选项，有时候效果好，有时候效果差
    loudness_envelope_adjustment = 1 # 输入源响度包络替换输出响度包络融合比例，越靠近1越使用输出响度包络

    if cluster_infer_ratio != 0:
        if feature_retrieval:  # 若指定了占比但没有指定模型路径，则按是否使用特征检索分配默认的模型路径
            cluster_model_path = model_dir + "/feature_and_index.pkl"
        else:
            cluster_model_path = model_dir + "/kmeans.pt"
    else:  # 若未指定占比，则无论是否指定模型路径，都将其置空以避免之后的模型加载
        cluster_model_path = ""

    svc_model = Svc(model_dir + "/G.pth",
                    model_dir + "/config.json",
                    "cpu",
                    cluster_model_path,
                    model_dir + "/diffusion.pt",
                    model_dir + "/diffusion.yaml",
                    enhance,
                    shallow_diffusion,
                    only_diffusion,
                    use_spk_mix,
                    feature_retrieval)

    for raw_audio_path in audio_path_list:
        if "." not in raw_audio_path:
            raw_audio_path += ".wav"
        infer_tool.format_wav(raw_audio_path)
        kwarg = {
            "raw_audio_path" : raw_audio_path,
            "spk" : spk,
            "tran" : 0,
            "slice_db" : slice_db,
            "cluster_infer_ratio" : cluster_infer_ratio,
            "auto_predict_f0" : auto_predict_f0,
            "noice_scale" : noice_scale,
            "pad_seconds" : pad_seconds,
            "clip_seconds" : clip,
            "lg_num": lg,
            "lgr_num" : lgr,
            "f0_predictor" : f0p,
            "enhancer_adaptive_key" : enhancer_adaptive_key,
            "cr_threshold" : cr_threshold,
            "k_step":k_step,
            "use_spk_mix": False,
            "second_encoding":second_encoding,
            "loudness_envelope_adjustment":loudness_envelope_adjustment
        }
        audio, total_time = svc_model.slice_inference(progressDict, key, **kwarg)
        soundfile.write(res_path, audio, svc_model.target_sample, format=wav_format)
        svc_model.clear_empty()
        return True