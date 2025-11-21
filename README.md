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
