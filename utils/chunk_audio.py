import os
from pydub import AudioSegment

def split_audio(filepath) :

    chunk_folder = "chunks"
    
    files = os.listdir(chunk_folder)

    # chunks/chunk_0001.wav/uplaods

    # 1. Delete old chunks

    for i in range(len(files)):
     file_path = os.path.join(chunk_folder, files[i])
     os.remove(file_path)

    # 2. Load uploaded audio
    audio = AudioSegment.from_wav(filepath)



    # 3. Split into chunks
    chunk_length = 3000
    chunk_count = 0
    for i in range(0, len(audio), chunk_length):
       
       chunk = audio[i:i + chunk_length]
       chunk_number = i // chunk_length
       chunk_count += 1
       
       filename = f"chunk_{chunk_number}.wav"
       
       file_path = os.path.join(chunk_folder, filename)
       
       chunk.export(file_path, format="wav")
    return chunk_count

    # 4. Save each chunk as chunk_0.wav, chunk_1.wav, ...

    # 5. Return number of chunks 

    