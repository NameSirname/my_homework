Хранилище всех моих программ, хоть сколько-нибудь стоящих хранения

Напоминания для меня в будущем: 

0) gcc -Wall -Wextra multifrac.c -lm -fopenmp -o a.o 

1) содержимое некоторых папок -- это одна программа или разные версии одной программы (версия отмечена другим названием/цифрой в конце) (=> (в отдельную папку) скачать всё содержимое этой папки и запустить прогу, импортирующую остальные). \

2) в папке jerunda заготовка к переписыванию всего на C/C++ с qt, для запуска может требоваться шаманство с .pro файлом (и не забыть про строчку "QT += widgets core gui")
для запуска: отредачить .pro файл, затем

qmake -o Makefile frac.pro

make
