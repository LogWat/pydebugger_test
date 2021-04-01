import my_debugger

debugger = my_debugger.debugger()

pid = input("Enter the PID of the process to attach to : ")

debugger.attach(int(pid))


list = debugger.enumerate_threads()

for i in list:
    thread_context = debugger.get_thread_context(i)
    print("[*] Dumping registers for thread ID: 0x{0:08x}".format((i)))
    print("[**] EIP: 0x{0:08x}".format((thread_context.Eip)))
    print("[**] ESP: 0x{0:08x}".format((thread_context.Esp)))
    print("[**] EBP: 0x{0:08x}".format((thread_context.Ebp)))
    print("[**] EAX: 0x{0:08x}".format((thread_context.Eax)))
    print("[**] EBX: 0x{0:08x}".format((thread_context.Ebx)))
    print("[**] ECX: 0x{0:08x}".format((thread_context.Ecx)))
    print("[**] EDX: 0x{0:08x}".format((thread_context.Edx)))
    print("[**] ESI: 0x{0:08x}".format((thread_context.Esi)))
    print("[**] EDI: 0x{0:08x}".format((thread_context.Edi)))
    print("[*] END DUMP")


debugger.detach()