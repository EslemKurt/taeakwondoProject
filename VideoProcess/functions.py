#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
import imageio


def head_sensor(video_path, csv_path, output_folder, f_frame_count=32, l_frame_count=16):
    # CSV dosyasını oku
    df = pd.read_csv(csv_path)

    # Başlangıç sistem zamanını al
    start_system_time = df[df['matchLogItemType'] == 'START_ROUND']['systemTime'].values[0]
    # Videoyu oku
    video = imageio.get_reader(video_path)
    fps = video.get_meta_data()['fps']
    frame_count = video.get_length()
    
    # c degisgeni kaydedilen pozision sayisini tutar
    c = 0

    # İlgili frame aralığını bul ve yeni video oluştur
    for index, row in df[(df['matchLogItemType'] == 'BLUE_HEAD_HIT') | (df['matchLogItemType'] == 'RED_HEAD_HIT')].iterrows():
        
        system_time = row['systemTime']
      

        # Sistem zamanını milisaniye cinsinden alıp, videonun zaman birimine çeviriyoruz
        video_time_seconds = (system_time - start_system_time) / 1000.0
       

        # Videonun zaman birimindeki zamanı frame sayısına çeviriyoruz
        frame_number = int(video_time_seconds * fps)
      
        frame_number = max(0, min(frame_count - 1, frame_number))  # Frame sayısını kontrol etme
     

        # İlk frame'den önceki ve sonraki frame'leri al
        start_frame = max(0, frame_number - f_frame_count)
  
        end_frame = min(frame_count - 1, frame_number + l_frame_count)
        c = c+1

        # Videoyu oku ve yeni videoya yaz
        output_video = []
        
        try:
            for i in range(start_frame, end_frame + 1):
                frame = video.get_data(i)
                output_video.append(frame)
             
        except IndexError as e:
            c = c-1
            print(f"Hata: {e}. Video uzunluğunu aşan bir indeksle karşılaşıldı. Video işleme devam ediliyor.")

        # Klasör kontrolü ve oluşturma
        os.makedirs(output_folder, exist_ok=True)
        
        # Oluşturulan videoyu belirtilen klasöre kaydet
        output_path = os.path.join(output_folder, f'head_sensor_{cam_num}_cam_{index+2}.mkv')
        output_writer = imageio.get_writer(output_path, fps=fps)
        for frame in output_video:
            output_writer.append_data(frame)
        output_writer.close()
    print(f'Sensorden algilanan kafa vuruslari {output_folder} dosyasina kaydedildi. Toplam {c} pozisyon.')


def head_scoreboard(video_path, csv_path, output_folder, f_sec=5):
    # CSV dosyasını oku
    df = pd.read_csv(csv_path)

    # Başlangıç sistem zamanını al
    start_system_time = df[df['matchLogItemType'] == 'START_ROUND']['systemTime'].values[0]

    # Videoyu oku
    video = imageio.get_reader(video_path)
    fps = video.get_meta_data()['fps']
    frame_count = video.get_length()
    
    # c degisgeni kaydedilen pozision sayisini tutar
    c = 0

    # İlgili frame aralığını bul ve yeni video oluştur
    for index, row in df.iterrows():
        match_log_type = row['matchLogItemType']
        entry_value = row['entryValue']

        if (match_log_type == 'BLUE_HEAD_POINT' or match_log_type == 'RED_HEAD_POINT') and entry_value == 'SCOREBOARD_EDITOR':
            system_time = row['systemTime']

            # TIMEOUT satırını bulma
            timeout_row = None
            for i in range(index - 1, -1, -1):
                if df.at[i, 'matchLogItemType'] == 'TIMEOUT':
                    timeout_row = df.iloc[i]
                    break

            if timeout_row is not None:
                timeout_system_time = timeout_row['systemTime']

                # Sistem zamanını milisaniye cinsinden alıp, videonun zaman birimine çeviriyoruz
                video_time_seconds = (timeout_system_time - start_system_time) / 1000.0

                # Videonun zaman birimindeki zamanı frame sayısına çeviriyoruz
                frame_number = int(video_time_seconds * fps)
                frame_number = max(0, min(frame_count - 1, frame_number))  # Frame sayısını kontrol etme

                # 5 saniye önceki frame'leri al
                start_frame = max(0, frame_number - int(f_sec * fps))
                end_frame = min(frame_count - 1, frame_number)
                c = c+1
                # Videoyu oku ve yeni videoya yaz
                output_video = []
                try:
                    for i in range(start_frame, end_frame + 1):
                        frame = video.get_data(i)
                        output_video.append(frame)
                except IndexError as e:
                    print(f"Hata: {e}. Video uzunluğunu aşan bir indeksle karşılaşıldı. Video işleme devam ediliyor.")
                    c = c-1
                # Klasör kontrolü ve oluşturma
                os.makedirs(output_folder, exist_ok=True)

                # Oluşturulan videoyu belirtilen klasöre kaydet
                output_path = os.path.join(output_folder, f'head_scoreboard_{cam_num}_cam_{index}.mkv')
                output_writer = imageio.get_writer(output_path, fps=fps)
                for frame in output_video:
                    output_writer.append_data(frame)
                output_writer.close()
    print(f'Scoreboardan eklenen kafa vuruslari {output_folder} dosyasina kaydedildi. Toplam {c} pozisyon.')



def rotation_judge(video_path, csv_path, output_folder, f_frame_count=92, l_frame_count=16):
    # CSV dosyasını oku
    df = pd.read_csv(csv_path)

    # Başlangıç sistem zamanını al
    start_system_time = df[df['matchLogItemType'] == 'START_ROUND']['systemTime'].values[0]

    # Videoyu oku
    video = imageio.get_reader(video_path)
    fps = video.get_meta_data()['fps']
    frame_count = video.get_length()
    
    # c degisgeni kaydedilen pozision sayisini tutar
    c = 0
    
    # İlgili frame aralığını bul ve yeni video oluştur
    for index, row in df[(df['matchLogItemType'] == 'RED_JUDGE_BODY_TECH') | (df['matchLogItemType'] == 'BLUE_JUDGE_BODY_TECH') | (df['matchLogItemType'] == 'RED_JUDGE_BODY_TECH') | (df['matchLogItemType'] == 'RED_JUDGE_HEAD_TECH')].iterrows():
        system_time = row['systemTime']

        # Sistem zamanını milisaniye cinsinden alıp, videonun zaman birimine çeviriyoruz
        video_time_seconds = (system_time - start_system_time) / 1000.0

        # Videonun zaman birimindeki zamanı frame sayısına çeviriyoruz
        frame_number = int(video_time_seconds * fps)
        frame_number = max(0, min(frame_count - 1, frame_number))  # Frame sayısını kontrol etme

        # Belirtilen sayıda önceki frame'leri al
        
        start_frame = max(0, frame_number - f_frame_count)
        end_frame = min(frame_count - 1, frame_number + l_frame_count)
        c = c+1
        # Videoyu oku ve yeni videoya yaz
        output_video = []
        try:
            for i in range(start_frame, end_frame + 1):
                frame = video.get_data(i)
                output_video.append(frame)
        except IndexError as e:
            print(f"Hata: {e}. Video uzunluğunu aşan bir indeksle karşılaşıldı. Video işleme devam ediliyor.")
            c = c-1

        # Klasör kontrolü ve oluşturma
        os.makedirs(output_folder, exist_ok=True)

        # Oluşturulan videoyu belirtilen klasöre kaydet
        output_path = os.path.join(output_folder, f'rotation_judge_{cam_num}_cam_{index}.mkv')
        output_writer = imageio.get_writer(output_path, fps=fps)
        for frame in output_video:
            output_writer.append_data(frame)
        output_writer.close()
    print(f'Yan hakemlerin isaretledikleri rotasyonlu vuruslar {output_folder} dosyasina kaydedildi. Toplam {c} pozisyon.')


def rotation_scoreboad(video_path, csv_path, output_folder, f_sec=5):
    # CSV dosyasını oku
    df = pd.read_csv(csv_path)

    # Başlangıç sistem zamanını al
    start_system_time = df[df['matchLogItemType'] == 'START_ROUND']['systemTime'].values[0]

    # Videoyu oku
    video = imageio.get_reader(video_path)
    fps = video.get_meta_data()['fps']
    frame_count = video.get_length()
    
    # c degisgeni kaydedilen pozision sayisini tutar
    c = 0
    
    # İlgili frame aralığını bul ve yeni video oluştur
    for index, row in df.iterrows():
        match_log_type = row['matchLogItemType']
        entry_value = row['entryValue']

        if (match_log_type in ['RED_BODY_TECH_POINT', 'RED_HEAD_TECH_POINT', 'BLUE_BODY_TECH_POINT', 'BLUE_HEAD_TECH_POINT']) and entry_value == 'SCOREBOARD_EDITOR':
            system_time = row['systemTime']

            # TIMEOUT satırını bulma
            timeout_row = None
            for i in range(index - 1, -1, -1):
                if df.at[i, 'matchLogItemType'] == 'TIMEOUT':
                    timeout_row = df.iloc[i]
                    break

            if timeout_row is not None:
                timeout_system_time = timeout_row['systemTime']

                # Sistem zamanını milisaniye cinsinden alıp, videonun zaman birimine çeviriyoruz
                video_time_seconds = (timeout_system_time - start_system_time) / 1000.0

                # Videonun zaman birimindeki zamanı frame sayısına çeviriyoruz
                frame_number = int(video_time_seconds * fps)
                frame_number = max(0, min(frame_count - 1, frame_number))  # Frame sayısını kontrol etme

                # Belirtilen sayıda önceki frame'leri al
                start_frame = max(0, frame_number - int(f_sec * fps))
                end_frame = min(frame_count - 1, frame_number)
                c = c+1
                # Videoyu oku ve yeni videoya yaz
                output_video = []
                try:
                    for i in range(start_frame, end_frame + 1):
                        frame = video.get_data(i)
                        output_video.append(frame)
                except IndexError as e:
                    print(f"Hata: {e}. Video uzunluğunu aşan bir indeksle karşılaşıldı. Video işleme devam ediliyor.")
                    c = c-1

                # Klasör kontrolü ve oluşturma
                os.makedirs(output_folder, exist_ok=True)

                # Oluşturulan videoyu belirtilen klasöre kaydet
                output_path = os.path.join(output_folder, f'rotation_scoreboad_{cam_num}_cam_{index}.mkv')
                output_writer = imageio.get_writer(output_path, fps=fps)
                for frame in output_video:
                    output_writer.append_data(frame)
                output_writer.close()
    print(f'Scoreboardan verilen rotasyonlu vuruslar {output_folder} dosyasina kaydedildi. Toplam {c} pozisyon.')


date='08_02'
court_num = 3
cam_num = 2

video_konum = f'/home/muhlabws4/videolar konya/cumakort3/Dışa Aktar 12-29-2023 6-48-32 PM/Medya yürütücüsü formatı/CAM-{cam_num}'
#video_name = '12_29_2023 5_49_59 PM (UTC+03_00).mkv'
video_name = '12_29_2023 5_50_00 PM (UTC+03_00).mkv'
video_path =f'{video_konum}/{video_name}'

csv_konum = f'/home/muhlabws4/Turkish_Open_2024_Antalya/{date}_2024/{court_num}th_court/matchlog'
csv_name = '08_02-347-1345.csv'
csv_path = f'{csv_konum}/{csv_name}'

output_path = f'/home/muhlabws4/Turkish_Open_2024_Antalya/{date}_2024/{court_num}th_court/cam_{cam_num}/{court_num}th_court_{cam_num}_cam_{date}'



head_sensor(video_path, csv_path, f'{output_path}_head_sensor', f_frame_count=32,l_frame_count=16,)



head_scoreboard(video_path, csv_path, f'{output_path}_head_scoreboard', f_sec=5)




rotation_judge(video_path, csv_path, f'{output_path}_rotation_judge', f_frame_count=92)




rotation_scoreboad(video_path, csv_path, f'{output_path}_rotation_scoreboard', f_sec=5)



