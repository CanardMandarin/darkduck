gcc --std=c99 CNC/*.c -o cnc.bin -Wall -g -DDEBUG  `mysql_config --cflags --libs`;
gcc --std=c99 BOT/*.c -o bot.bin -Wall -g -DDEBUG;