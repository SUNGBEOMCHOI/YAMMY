import os
import re
import json
import zipfile

class Aihub():
    def __init__(self, ):
        pass

    @staticmethod
    def label_preprocess(origin_path, new_path):
        sample_list = []
        with open(origin_path, 'rb') as f:
            while True:
                line = f.readline()
                if not line: break
                line = line.decode('utf-8')
                file_path, text =  line.split(" :: ")
                text = re.sub(r'\n', '', text)
                text = re.sub(r'\((.*?)\)\/\(([^\(]*)\)', r'\1',  text)
                text = re.sub(r'[a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣ]\/\s*', '', text)
                text = re.sub(r'[a-zA-Z0-9가-힇ㄱ-ㅎㅏ-ㅣ]*\+\s*', '', text)
                text = re.sub(r'[!@#$%^&*_?,<>`~.]', '', text)

                sample_list.append({"wav":file_path, "text":text, "speaker_id":"0"})
        with open(new_path, 'w', encoding='UTF-8-sig') as f:
            json.dump(sample_list, f, indent=2, ensure_ascii=False)

    @staticmethod
    def car_label_preprocess(origin_path, new_path):
        new_sample_list = []
        with open(origin_path, 'r', encoding='UTF-8-sig') as f:
            sample_list = json.load(f)
            for sample in sample_list:
                text = sample['text']                
                text = text.replace('?', '')
                text = text.replace('!', '')
                new_sample_list.append({"wav":sample['wav'], "text":text, "speaker_id":"0"})
        with open(new_path, 'w', encoding='UTF-8-sig') as f:
            json.dump(new_sample_list, f, indent=2, ensure_ascii=False)


    @staticmethod
    def extract_zip(path, new_path):
        if os.path.isdir(path):
            directory_path = path
            zip_path_list = os.listdir(directory_path)

            for zip_path in zip_path_list:
                name, ext = os.path.splitext(zip_path)
                if ext == '.zip':
                    full_zip_path = os.path.join(directory_path, zip_path)
                    print(f'Current Unziped file : {full_zip_path}')
                    zipfile.ZipFile(full_zip_path).extractall(new_path)
        else:
            zip_path = path
            print(f'Current Unziped file : {zip_path}')
            zipfile.ZipFile(zip_path).extractall(new_path)

    @staticmethod
    def car_conversation_label_preprocess(directory_path, wav_directory, save_file_path, istrain):
        sample_list = []
        sub_sub_directory_path_list = os.listdir(directory_path)
        for sub_sub_directory_path in sub_sub_directory_path_list:
            dataset_type = sub_sub_directory_path
            label_type = 'train' if istrain else 'validation'
            print(sub_sub_directory_path)
            if dataset_type == 'sec':
                exist_check_path = f'../data/aihub_car/data/{label_type}/AI비서'
            elif dataset_type == 'h2c':
                exist_check_path = f'../data/aihub_car/data/{label_type}/홈투카'
            elif dataset_type == 'self':
                exist_check_path = f'../data/aihub_car/data/{label_type}/자율주행'
            elif dataset_type == 'c2h':
                exist_check_path = f'../data/aihub_car/data/{label_type}/카투홈'
            sub_directory_path_list = os.listdir(os.path.join(directory_path, sub_sub_directory_path))
            for sub_directory_path in sub_directory_path_list:
                if os.path.isdir(exist_check_path + '/' + sub_directory_path):
                    label_directory_path = os.path.join(os.path.join(directory_path, sub_sub_directory_path, sub_directory_path))
                    label_path_list = os.listdir(label_directory_path)
                    for label_path in label_path_list:
                        full_label_path = os.path.join(label_directory_path, label_path)
                        with open(full_label_path, 'r', encoding='UTF-8-sig') as file:
                            data = json.load(file)
                            file_path = '/'.join([label_path.split('-')[0], label_path]) # ex) EA_0370/EA_0370-501-04-01-LOH-F-08-A.json
                            if dataset_type == 'sec':
                                file_path = '/'.join(['AI비서', file_path]) # 'AI비서/EA_0370/EA_0370-501-04-01-LOH-F-08-A.json'
                            elif dataset_type == 'h2c':
                                file_path = '/'.join(['홈투카', file_path])
                            elif dataset_type == 'self':
                                file_path = '/'.join(['자율주행', file_path])
                            elif dataset_type == 'c2h':
                                file_path = '/'.join(['카투홈', file_path])
                            file_path = '/'.join([wav_directory, file_path]) # 'train/AI 비서/EA_0370-501-04-01-LOH-F-08-A.json'
                            file_path = file_path[:-4] + 'wav' # 'train/AI 비서/EA_0370-501-04-01-LOH-F-08-A.wav'

                            text = data['전사정보']['LabelText']

                            sample_list.append({"wav":file_path, "text":text, "speaker_id":"0"})

        with open(save_file_path, 'w', encoding='UTF-8-sig') as f:
            json.dump(sample_list, f, indent=2, ensure_ascii=False)
            print(f"{len(sample_list)} Samples collected")

    @staticmethod
    def aihub_bus_label_preprocess(origin_directory, save_file_path):
        sample_list = []
        wav_file_list = os.listdir(origin_directory)
        print(len(wav_file_list))
        for wav_file in wav_file_list:
            name, ext = os.path.splitext(wav_file)
            if name[-2:] == 'SD':
                file_path = os.path.join(origin_directory, wav_file)
                sample_list.append({"wav":file_path, "text":"", "speaker_id":"0"})
        with open(save_file_path, 'w', encoding='UTF-8-sig') as f:
            json.dump(sample_list, f, indent=2, ensure_ascii=False)
            print(f"{len(sample_list)} Samples collected")
        
        


if __name__ == "__main__":
    #################################
    #              Unzip            #
    #################################
    # directory_path = '../data/aihub_car_zip/scripts/validation'
    # new_path = '../data/aihub_car/scripts/validation'
    # Aihub.extract_zip(directory_path, new_path)
        
    #################################
    #      Aihub label process      #
    #################################
    # Aihub.label_preprocess('./data/aihub/scripts/eval_other.trn',
    #  './data/aihub/scripts/eval_other.json')

    #################################
    #    Aihub car label process    #
    #################################
    # directory_path = '../data/aihub_car/scripts/validation'
    # wav_directory = './validation'
    # save_file_path = '../data/aihub_car/scripts/all_validation.json'
    # Aihub.car_conversation_label_preprocess(directory_path, wav_directory, save_file_path, istrain=False)

    #################################
    #    Aihub car label process    #
    #################################
    # origin_path = '../data/aihub_car/scripts/all_train.json'
    # new_path = '../data/aihub_car/scripts/train.json'
    # Aihub.car_label_preprocess(origin_path, new_path)

    #################################
    #    Aihub bus label process    #
    #################################
    origin_path = '/root/data/aihub_bus/06.지하철,버스/04.버스안'
    save_file_path = '/root/data/aihub_bus/scripts/sd.json'
    Aihub.aihub_bus_label_preprocess(origin_path, save_file_path)