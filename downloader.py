import os
import requests
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TaskID, TimeRemainingColumn
from error import *

def download(url:str, filePath:str, fileExt,  header:dict, session:requests.Session, chunk_size=8192):
    if not os.path.isdir(os.path.dirname(filePath)):
        print("Path does not exist! Create the path %s and then try again"%(os.path.dirname(filePath)))
        exit()
    try:
        session.headers.update(header)
        response = session.get(url, headers=header, stream=True)
        response.raise_for_status()  # Check if the request was successful
        total_size = int(response.headers.get('content-length', 0))

        # Configure Rich Progress
        progress = Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            transient=True,
        )
        task_id = TaskID(filePath[:20]+'...'+fileExt)
        task = progress.add_task(task_id, total=total_size)

        with open(filePath, 'wb') as file:
            progress.start()
            for chunk in response.iter_content(chunk_size=chunk_size):
                file.write(chunk)
                progress.update(task, advance=len(chunk))
            progress.stop()
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")