CC = gcc
CFLAGS = -fpic $(OPTFLAGS)
LDFLAGS = -shared -ldl

all: unset_var.so

%.so : %.o
	$(CC) $(CFLAGS) $(LDFLAGS) $< -o $@

clean:
	rm -f *.so *.o

.SECONDARY:
