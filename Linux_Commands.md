# Linux

### name -a

The `uname -a` command in Ubuntu (or any Unix-like operating system) displays detailed information about the system's kernel and hardware. Specifically, it prints the following information:

1. **Kernel Name**: The name of the operating system kernel (e.g., Linux).
2. **Node Name**: The hostname of the machine.
3. **Kernel Release**: The version of the kernel release.
4. **Kernel Version**: The version of the kernel, including any additional information about the build.
5. **Machine Hardware Name**: The hardware architecture of the machine (e.g., x86_64 for 64-bit Intel/AMD processors).
6. **Processor Type**: The type of processor or instruction set architecture.
7. **Operating System**: The name of the operating system (e.g., GNU/Linux).

Here's an example output of the `uname -a` command on an Ubuntu system:

```
$ uname -a
Linux hostname 5.4.0-126-generic #142-Ubuntu SMP Fri Apr 15 17:31:46 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
```

In this example:

- `Linux` is the kernel name.
- `ip-172-31-19-22` is the node name (hostname of the machine).
- `5.15.0-1052-aws` is the kernel release version.
- `#57-20.04.1-Ubuntu SMP Mon Jan 15 17:04:56 UTC 2024` is additional information about the kernel version and build.
- `x86_64` is the machine hardware name (64-bit architecture).
- `x86_64` is the processor type (also 64-bit).
- `GNU/Linux` is the operating system name.

The `uname -a` command is useful for quickly getting a comprehensive overview of the system's kernel and hardware details, which can be helpful for troubleshooting, system administration, or verifying that the correct kernel and architecture are being used.



### sudo service xxx start/stop

`sudo service mysql stop`

`sudo service mongod start`



### `mysql -u root -p`