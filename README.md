# Puzzlecat - Hashcat Bitcoin Brainwallet Modules

Custom hashcat modules for cracking Bitcoin brainwallet addresses using GPU acceleration.

## Overview

This repository contains custom hashcat modules for Bitcoin brainwallet address generation and cracking. It supports both compressed and uncompressed Bitcoin addresses derived from passphrases.

## Modules

### Module 01337 - Brainwallet (Uncompressed)
- **Hash Mode**: 1337
- **Description**: Cracks uncompressed Bitcoin P2PKH addresses generated from brainwallets
- **Files**:
  - `custom-module/module_01337.c` - Host-side module implementation
  - `custom-kernel/m01337-pure.cl` - OpenCL kernel for GPU acceleration

### Module 01338 - Brainwallet (Compressed)
- **Hash Mode**: 1338
- **Description**: Cracks compressed Bitcoin P2PKH addresses generated from brainwallets
- **Files**:
  - `custom-module/module_01338.c` - Host-side module implementation
  - `custom-kernel/m01338-pure.cl` - OpenCL kernel for GPU acceleration

## How It Works

Both modules implement the following process:

1. **Input**: A passphrase candidate
2. **SHA-256**: Hash the passphrase to generate a private key
3. **SECP256k1**: Perform elliptic curve point multiplication (private key × G) to get the public key
4. **Public Key Formatting**:
   - Module 01337: Uses uncompressed format (65 bytes, prefix 0x04)
   - Module 01338: Uses compressed format (33 bytes, prefix 0x02 or 0x03)
5. **HASH160**: Apply SHA-256 followed by RIPEMD-160 to the public key
6. **Base58Check**: Encode with version byte (0x00 for mainnet) to produce Bitcoin address
7. **Comparison**: Compare against target addresses

## Target Hashes

Example target hashes are provided in the `targets/` directory:
- `targets/hashes-uc.hashes` - Uncompressed address targets for module 01337
- `targets/hashes-c.hashes` - Compressed address targets for module 01338

## Installation & Usage

### Installing into Hashcat

1. **Copy module files** to your hashcat installation:
   ```bash
   # Copy C modules
   cp custom-module/module_01337.c /path/to/hashcat/src/modules/
   cp custom-module/module_01338.c /path/to/hashcat/src/modules/
   
   # Copy OpenCL kernels
   cp custom-kernel/m01337-pure.cl /path/to/hashcat/OpenCL/
   cp custom-kernel/m01338-pure.cl /path/to/hashcat/OpenCL/
   ```

2. **Rebuild hashcat** to include the custom modules:
   ```bash
   cd /path/to/hashcat
   make clean
   make
   ```

### Running with GPU Acceleration

The modules automatically use GPU acceleration via OpenCL. All expensive operations (SHA-256, SECP256k1 elliptic curve math, RIPEMD-160) run on the GPU.

Example hashcat commands:
```bash
# For uncompressed addresses (module 1337)
hashcat -m 1337 -a 3 hashes-uc.hashes ?a?a?a?a?a?a?a?a

# For compressed addresses (module 1338)
hashcat -m 1338 -a 3 hashes-c.hashes ?a?a?a?a?a?a?a?a

# Use specific GPU devices
hashcat -m 1337 -d 1,2 -a 3 hashes-uc.hashes ?a?a?a?a?a?a

# Monitor GPU workload
hashcat -m 1337 -I --benchmark
```

## Performance Optimization

### Maximize Speed Without Quality Loss

**1. Workload Tuning**
```bash
# Increase workload profile for maximum GPU utilization
hashcat -m 1337 -w 3 hashes.txt wordlist.txt  # High workload
hashcat -m 1337 -w 4 hashes.txt wordlist.txt  # Nightmare mode (maximum speed)
```

**2. Kernel Optimization**
```bash
# Fine-tune kernel parameters (benchmark different values for your GPU)
hashcat -m 1337 -n 1024 -u 256 hashes.txt wordlist.txt
# -n: Number of kernel threads (try: 256, 512, 1024)
# -u: Kernel loops (try: 64, 128, 256, 512)

# Auto-tune to find optimal values
hashcat -m 1337 --benchmark --force
```

**3. Multi-GPU Scaling**
```bash
# Utilize all available GPUs
hashcat -m 1337 -d 1,2,3,4 hashes.txt wordlist.txt

# Balance load across GPUs
hashcat -m 1337 -d 1,2 --gpu-temp-abort=90 hashes.txt wordlist.txt
```

**4. Smart Attack Strategies**
```bash
# Dictionary attack with rules (faster than pure brute force)
hashcat -m 1337 -a 0 hashes.txt wordlist.txt -r rules/best64.rule
hashcat -m 1337 -a 0 hashes.txt wordlist.txt -r rules/dive.rule

# Hybrid attacks: dictionary + mask
hashcat -m 1337 -a 6 hashes.txt wordlist.txt ?d?d?d?d       # Append digits
hashcat -m 1337 -a 7 hashes.txt ?d?d?d?d wordlist.txt       # Prepend digits

# Focused character sets (10-100x faster than ?a for known patterns)
hashcat -m 1337 -a 3 -1 ?l?u?d hashes.txt ?1?1?1?1?1?1?1?1  # Alphanumeric only
hashcat -m 1337 -a 3 -1 ?l?d hashes.txt ?1?1?1?1?1?1?1?1    # Lowercase + digits
```

**5. Session Management**
```bash
# Save/restore sessions for long-running attacks
hashcat -m 1337 --session=mysession hashes.txt wordlist.txt
hashcat --session=mysession --restore

# Use potfile to avoid rechecking found passwords
hashcat -m 1337 --potfile-path=found.pot hashes.txt wordlist.txt
```

**6. Hardware Optimization**
- **Cooling**: Ensure proper GPU cooling (thermal throttling reduces speed by 30-50%)
- **Power**: Use adequate PSU and enable performance mode
- **PCIe**: Use PCIe 3.0/4.0 x16 slots for maximum bandwidth
- **Overclocking**: Carefully OC memory and core (5-15% speed gain)
- **Multiple GPUs**: Linear scaling up to 4 GPUs, diminishing returns beyond that

**7. System Optimization**
```bash
# Reduce system load
hashcat -m 1337 --force --opencl-device-types=2 hashes.txt wordlist.txt  # GPU only

# Disable screen output for slight speed boost
hashcat -m 1337 --quiet hashes.txt wordlist.txt
```

**Performance Expectations:**
- **Single RTX 3090**: ~50-100 MH/s (depends on password length)
- **Single RTX 4090**: ~80-150 MH/s
- **Quad RTX 4090**: ~300-500 MH/s (near-linear scaling)

**Note**: SECP256k1 elliptic curve operations are computationally intensive. Performance is limited by the mathematical operations, not the implementation.

## Technical Details

- **Algorithm**: SECP256k1 elliptic curve cryptography
- **Hash Functions**: SHA-256, RIPEMD-160
- **Encoding**: Base58Check
- **Attack Mode**: Outside kernel (GPU computation with CPU-side Base58Check validation)
- **Password Length**: 1-64 characters
- **GPU Acceleration**: SHA-256, SECP256k1 point multiplication, and RIPEMD-160 all run on GPU
- **Performance**: Scales with GPU compute capability (CUDA cores/Stream processors)

## License

MIT License - See file headers for details

## Credits

Based on the hashcat framework. See `docs/credits.txt` for full attribution.

## Security Note

These tools are for educational and security research purposes only. Use responsibly and only on systems you own or have explicit permission to test.
