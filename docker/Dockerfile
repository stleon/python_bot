FROM python:slim

RUN pip install jupyter
RUN apt-get update && apt-get install -y vim

EXPOSE 10001 10002 10003 10004 10005

RUN /bin/bash -c 'echo -e "\n\
ulimit -c 0  # Запрещаем создавать core файлы\n\
ulimit -d 64000  # Ограничиваем максимальный размер сегмента данных в 64 MB \n\
ulimit -s 8192  # Ограничиваем максимальный размер стэка в 8 MB \n\
ulimit -m 64000  # Ограничиваем максимальный размер резидентной части процесса (находящейся в ОЗУ) в  64 MB \n\
ulimit -u 164  # Ограничиваем максимальное число запущенных этим пользователем процессов. \n\
ulimit -n 164  # Ограничиваем максимальное число открытых файлов. \n\
ulimit -f 64000  # Ограничиваем максимальный размер создаваемого файла в 64 MB \n\
ulimit -v 64000  # Ограничиваем максимальный размер используемой виртуальной памяти в 64 MB" \
>> /etc/bash.bashrc'

RUN /bin/bash -c 'echo -e "\n\
set editing-mode vi \n\
set keymap vi \n\

set bell-style none \n\
$if mode=vi \n\
    set keymap vi-command \n\
    "gg": beginning-of-history \n\
    "G": end-of-history \n\
    set keymap vi-insert \n\
    "jj": vi-movement-mode \n\
    "\C-w": backward-kill-word \n\
    "\C-p": history-search-backward \n\
$endif" \
>> /etc/inputrc'


